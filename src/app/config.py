from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения."""

    kafka_host: str = 'kafka'
    kafka_port: str = '9092'
    kafka_consumer_topics: str = 'faces'
    kafka_instance: str = f'{kafka_host}:{kafka_port}'
    file_encoding: str = 'utf-8'


settings = Settings()
