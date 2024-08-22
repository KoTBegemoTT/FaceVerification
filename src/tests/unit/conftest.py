import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_helper import DatabaseHelper
from app.db.models import BaseTable, User

TEST_DB_URL = 'postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/test_db'  # noqa: E501
test_db_helper = DatabaseHelper(url=TEST_DB_URL, echo=True)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_db_helper.session_factory() as session:
        yield session


@pytest_asyncio.fixture()
async def reset_db():
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.create_all)
    yield
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(BaseTable.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def db_helper():
    return test_db_helper


@pytest_asyncio.fixture()
async def user() -> User:
    async with test_db_helper.session_factory() as session:
        user = User(name='user', password=b'password')
        session.add(user)
        await session.commit()
        return user
