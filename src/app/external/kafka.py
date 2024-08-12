import logging

import brotli
from aiokafka import AIOKafkaConsumer

from app.config import settings
from app.face_verification.views import image_to_vector

log = logging.getLogger('uvicorn')

verificated_users: set[int] = set()


async def create_consumer() -> AIOKafkaConsumer:
    """Создание объекта KafkaConsumer."""
    return AIOKafkaConsumer(
        settings.kafka_consumer_topics,
        bootstrap_servers=settings.kafka_instance,
    )


async def decompress(file_bytes: bytes) -> str:
    """Декомпрессия сообщения."""
    return str(brotli.decompress(file_bytes), settings.file_encoding)


async def consume(consumer: AIOKafkaConsumer) -> None:
    """Обработка сообщений из кафки."""
    async for msg in consumer:
        file_path = await decompress(msg.value)
        user_id = int(await decompress(msg.key))

        verificated_users.add(user_id)

        vector = await image_to_vector(file_path)
        log.info(f'{user_id=} {vector=}')
