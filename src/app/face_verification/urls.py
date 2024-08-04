from fastapi import APIRouter, status

from app.face_verification.views import image_to_vector  # type: ignore

router = APIRouter(tags=['face_verification'])


@router.get(
    '/healthz/ready/',
    status_code=status.HTTP_200_OK,
)
async def ready_check() -> bool:
    """Проверка состояния сервиса."""
    return True


@router.get(
    '/get_vector/',
    status_code=status.HTTP_200_OK,
)
async def create_transaction(path: str) -> list[float]:
    """Создание новой транзакции."""
    return await image_to_vector(path)
