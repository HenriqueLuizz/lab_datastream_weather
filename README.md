# LAB DATA STREAM WEATHER

O objetivo deste lab é subir um producer kafka que emite dados de temperatura, humidade de forma aleatória e os dados são recebidos por um consumer kafka que agrupa em intervalos preconfigurados e grava no MinIO no formato de Parquet.
Este projeto implementa um pipeline de processamento de streaming utilizando Apache Kafka para ingestão de dados e MinIO para armazenamento dos dados processados no formato Parquet.

## Arquitetura do Projeto

O projeto é composto pelos seguintes serviços:

- **Zookeeper**: Coordena os brokers do Kafka.
- **Kafka**: Middleware de mensagens para ingestão de dados.
- **Kafka UI**: Interface gráfica para monitoramento do Kafka.
- **MinIO**: Armazena os dados processados no formato Parquet.
- **Weather Producer**: Envia mensagens simuladas para o tópico `weather_stream` do Kafka.
- **Weather Consumer**: Consome as mensagens do tópico e salva no MinIO em Parquet.

## Tecnologias Utilizadas

- Docker & Docker Compose
- Apache Kafka
- Apache Zookeeper
- MinIO (compatível com Amazon S3)
- Python (com `kafka-python`, `pandas`, `pyarrow`, `s3fs`)
- Kafka UI (para monitoramento dos tópicos)

## Como Executar

### **Clone o Repositório**

```bash
git clone https://github.com/HenriqueLuizz/lab_datastream_weather.git
cd lab_datastream_weather
```

### **Suba os Contêineres**

`docker-compose up -d`

> Observação: Certifique-se de que as portas 9092, 2181, 8080, 9000 e 9001 estão livres.

### Verifique os Logs dos Serviços

`docker-compose logs -f weather_producer`
`docker-compose logs -f weather_consumer`

### Acesse a Interface do Kafka UI

Após iniciar os contêineres, acesse a interface web do Kafka UI:

> http://localhost:8080

Aqui você pode monitorar a chegada das mensagens no tópico weather_stream.

### Testando o Armazenamento no MinIO

Após o consumer processar os dados, eles serão armazenados no MinIO.

> Acesse o Console do MinIO: http://localhost:9001
Login: minioadmin
Senha: minioadmin
Bucket de armazenamento: datalake

Você pode visualizar os arquivos Parquet gerados diretamente no bucket.

### Estrutura dos Arquivos

/lab_datastream_weather/
│-- docker-compose.yaml
│-- dockerfile.producer
│-- dockerfile.consumer
│-- README.md
│-- kafka_producer.py
│-- kafka_consumer.py

### Configurações Importantes

#### Kafka

O weather_producer publica mensagens no Kafka, que são consumidas pelo weather_consumer.

O broker do Kafka está acessível pelo endereço:
kafka:29092 (interno)
localhost:9092 (externo)

#### MinIO

Os dados processados são armazenados no bucket datalake.

Credenciais padrão:
    Usuário: minioadmin
    Senha: minioadmin

#### Como Parar os Contêineres

docker-compose down
