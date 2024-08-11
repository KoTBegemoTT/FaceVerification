import asyncio
from contextlib import asynccontextmanager
import hashlib
import logging
import uvicorn
from fastapi import FastAPI
from aiokafka import AIOKafkaConsumer
import brotli

from app.external.kafka import consume, create_consumer
from app.face_verification.urls import router  # type: ignore


@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer = await create_consumer()
    await consumer.start()
    asyncio.create_task(consume(consumer))

    yield

    await consumer.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(router)


@app.get('/')
async def root():
    """Стартовая страница."""
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        workers=2,
        reload=True,
        host='0.0.0.0',  # noqa: S104
        port=8003,  # noqa: WPS432
    )
