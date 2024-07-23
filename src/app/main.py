import uvicorn
from fastapi import FastAPI

from app.face_verification.urls import router as verification_router  # type: ignore

app = FastAPI()
app.include_router(verification_router)


@app.get('/')
async def root():
    """Стартовая страница."""
    return {'message': 'Hello World'}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        reload=True,
        host='0.0.0.0',  # noqa: S104
        port=8000,  # noqa: WPS432
    )
