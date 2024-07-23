from fastapi import APIRouter, status

from app.face_verification.views import image_to_vector

router = APIRouter(tags=['face_verification'])


@router.get(
    '/get_vector',
    status_code=status.HTTP_200_OK,
)
def create_transaction(path: str) -> list[float]:
    """Создание новой транзакции."""
    return image_to_vector(path)
