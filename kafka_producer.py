import os
import json
import time
import logging
from kafka import KafkaProducer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
TOPIC_NAME = os.environ.get("TOPIC_NAME", "weather_stream")

# Configurar o Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),  # Serializa como JSON
    client_id="weather_producer"
)

def generate_message():
    """Gera uma mensagem de exemplo."""
    return {
        "temperature": round(20 + 5 * (0.5 - time.time() % 1), 2),
        "humidity": round(50 + 10 * (0.5 - time.time() % 1), 2),
        "timestamp": time.time()
    }

logger.info(f"Producing messages to Kafka topic '{TOPIC_NAME}' on broker '{KAFKA_BROKER}'...")

try:
    while True:
        message = generate_message()
        producer.send(TOPIC_NAME, value=message)
        logger.info(f"Sent: {message}")
        producer.flush()
        time.sleep(2)  # Simula um delay entre mensagens
except KeyboardInterrupt:
    logger.warning("Producer interrompido pelo usuário.")
finally:
    producer.close()
    logger.info("Producer encerrado.")
