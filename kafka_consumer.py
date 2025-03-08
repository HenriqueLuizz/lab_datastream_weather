import os
import json
import logging
import pandas as pd
import pyarrow.parquet as pq
import s3fs
from kafka import KafkaConsumer
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Configurações do Kafka
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = "weather_stream"

# Configurações do MinIO
MINIO_URL = os.environ.get("MINIO_URL", "http://localhost:9000")
MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "minioadmin") # Está aqui apenas para simplificar o LAB
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = "datalake"
PARQUET_PATH = f"{MINIO_BUCKET}/"  # Caminho no MinIO

# Inicializa o consumer Kafka
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="weather_consumer_group"
)

# Inicializa o sistema de arquivos MinIO via S3
s3 = s3fs.S3FileSystem(
    client_kwargs={"endpoint_url": MINIO_URL},
    key=MINIO_ACCESS_KEY,
    secret=MINIO_SECRET_KEY
)

logger.info(f"Listening for messages on topic '{TOPIC_NAME}' from broker '{KAFKA_BROKER}'...")

# Lista para armazenar as mensagens antes de salvar no Parquet
batch_data = []
BATCH_SIZE = 10  # Define quantas mensagens acumular antes de salvar

try:
    for message in consumer:
        data = message.value
        logger.info(f"Received: {data}")

        batch_data.append(data)

        # Se atingir o tamanho do batch, salva no MinIO
        if len(batch_data) >= BATCH_SIZE:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"weather_data_{timestamp}.parquet"
            df = pd.DataFrame(batch_data)  # Converte lista para DataFrame

            try:
                with s3.open(PARQUET_PATH + file_name, "wb") as f:
                    df.to_parquet(f, engine="pyarrow", index=False)
                logger.info(f"✅ {file_name} salvo em {PARQUET_PATH}")
            except Exception as e:
                logger.error(f"Erro ao salvar arquivo no MinIO: {e}")

            batch_data = []

except KeyboardInterrupt:
    logger.warning("Consumer interrompido pelo usuário.")
finally:
    consumer.close()
    logger.info("Consumer encerrado.")
