import asyncio
import hashlib
import logging
from aiokafka import AIOKafkaConsumer
from app.config import settings
import brotli
import aiofiles

from app.face_verification.views import image_to_vector

log = logging.getLogger("uvicorn")

verificated_users: set[int] = set()


async def create_consumer() -> AIOKafkaConsumer:
    return AIOKafkaConsumer(
        settings.kafka_consumer_topics,
        bootstrap_servers=settings.kafka_instance,
    )


async def decompress(file_bytes: bytes) -> str:
    return str(brotli.decompress(file_bytes), settings.file_encoding)


async def consume(consumer: AIOKafkaConsumer) -> None:
    """Обработка сообщения из кафки."""
    async for msg in consumer:
        mesage = await decompress(msg.value)
        id_str, file_path = mesage.split(':')
        id = int(id_str)
        verificated_users.add(id)
        vector = await image_to_vector(file_path)
        log.info(vector)
