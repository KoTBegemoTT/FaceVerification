import hashlib
import logging
import uvicorn
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import brotli

from app.face_verification.urls import router  # type: ignore

app = FastAPI()
app.include_router(router)


async def start_consumer() -> AIOKafkaConsumer:
    consumer = AIOKafkaConsumer('faces', bootstrap_servers='kafka:9092')
    await consumer.start()
    return consumer

# def create_consumer() -> AIOKafkaConsumer:
#     return AIOKafkaConsumer('faces', bootstrap_servers='kafka:9092')

log = logging.getLogger("uvicorn")


async def decompress(file_bytes: bytes) -> str:
    """Decompress message from Kafka.

    Args:
        file_bytes (bytes): Kafka message bytes.

    Returns:
        AIOKafkaConsumer: Decompressed Kafka message (string).
    """

    return str(
        brotli.decompress(file_bytes),
        'utf-8',
    )


async def consume():
    """Consume and print messages from Kafka."""
    consumer = await start_consumer()

    while True:
        async for msg in consumer:
            decompressed = await decompress(msg.value)
            with open(decompressed, 'rb') as file:
                image_data = file.read()
            print(
                "consumed: ",
                f"topic: {msg.topic},",
                f"partition: {msg.partition},",
                f"offset: {msg.offset},",
                f"key: {msg.key},",
                f"value: {decompressed},",
                f"timestamp: {msg.timestamp}",
                f"hash_value: {hashlib.sha256(image_data).hexdigest()}",
            )


@app.on_event("startup")
async def startup_event():
    """Start up event for FastAPI application."""

    log.info("Starting up...")
    # await consumer.start()
    await consume()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event for FastAPI application."""

    log.info("Shutting down...")
    # await consumer.stop()


@app.get('/')
async def root():
    """Стартовая страница."""
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True,
        host='0.0.0.0',  # noqa: S104
        port=8003,  # noqa: WPS432
    )
