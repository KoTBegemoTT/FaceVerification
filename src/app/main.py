import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, status

from app.external.kafka import consume, create_consumer
from app.face_verification.urls import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Настройки запуска и остановки сервиса."""
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


@app.get('/ready', status_code=status.HTTP_200_OK)
async def ready_check():
    """Проверка состояния сервиса."""
    return {'message': 'Service is ready'}


@app.get('/live', status_code=status.HTTP_200_OK)
async def live_check():
    """Проверка состояния сервиса."""
    return {'message': 'Service is live'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        workers=1,
        reload=True,
        host='0.0.0.0',  # noqa: S104
        port=8003,  # noqa: WPS432
    )
