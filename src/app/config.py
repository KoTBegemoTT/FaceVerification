from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация приложения."""

    # Настройки kafka
    kafka_host: str = 'kafka'
    kafka_port: str = '9092'
    kafka_consumer_topic: str = 'faces'
    file_encoding: str = 'utf-8'

    # Настройки db
    db_user: str = 'postgres'
    db_password: str = 'postgres'
    db_host: str = 'host.docker.internal'
    db_port: str = '5432'
    db_name: str = 'credit_card'
    db_echo: bool = False
    db_schema: str = 'lebedev_schema'

    @property
    def db_url(self) -> str:
        """Ссылка на БД."""
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'  # noqa: E501, WPS221

    @property
    def kafka_instance(self) -> str:
        """Ссылка на kafka."""
        return f'{self.kafka_host}:{self.kafka_port}'


settings = Settings()
