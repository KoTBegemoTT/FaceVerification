import uvicorn
from fastapi import FastAPI

from app.face_verification.urls import router  # type: ignore

app = FastAPI()
app.include_router(router)


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
