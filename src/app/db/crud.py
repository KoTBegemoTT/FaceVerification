from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


async def get_user_by_id(user_id: int, session) -> User:
    """Получение пользователя по ID."""
    return await session.get(User, user_id)


async def set_user_verified(
    user_id: int,
    vector: list[float],
    session: AsyncSession,
) -> None:
    """Установка пользователя как верифицированного."""
    user = await get_user_by_id(user_id, session)
    user.is_verified = True
    user.verification_vector = vector

    await session.commit()
