import hashlib
from aiokafka import AIOKafkaConsumer
from app.config import settings
import brotli
import aiofiles

consumer = AIOKafkaConsumer(
    settings.kafka_topics,
    bootstrap_servers=settings.kafka_instance,
)


async def decompress(file_bytes: bytes) -> str:
    return str(brotli.decompress(file_bytes), settings.file_encoding)


async def consume():
    """Consume and print messages from Kafka."""

    while True:
        async for msg in consumer:
            file_path = await decompress(msg.value)
            async with aiofiles.open(file_path, 'rb') as file:
                image_data = file.read()
            print(
                "consumed: ",
                f"topic: {msg.topic},",
                f"partition: {msg.partition},",
                f"offset: {msg.offset},",
                f"key: {msg.key},",
                f"value: {await decompress(msg.value)},",
                f"timestamp: {msg.timestamp}",
                f"hash_value: {hashlib.sha256(image_data).hexdigest()}",
            )
