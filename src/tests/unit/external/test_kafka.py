import logging
from unittest.mock import Mock

import brotli
import pytest
from aiokafka import AIOKafkaConsumer

from app.config import settings
from app.db.models import User
from app.external.kafka import consume, create_consumer, decompress


class ConsumerMock:
    def __init__(self, mesages):
        self._messages = mesages
        self.start = 0
        self.end = len(mesages)

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self.start >= self.end:
            raise StopAsyncIteration

        value = self._messages[self.start]
        self.start += 1
        return value


@pytest.mark.asyncio
async def test_create_consumer():
    consumer = await create_consumer()

    assert isinstance(consumer, AIOKafkaConsumer)


@pytest.mark.asyncio
async def test_decompress():
    message = '1:src/tests/images/image_for_vectorise.jpeg'
    compressed = brotli.compress(message.encode(settings.file_encoding))
    assert await decompress(compressed) == message


@pytest.mark.parametrize(
    'message_value',
    [
        pytest.param(
            'src/tests/images/image_for_vectorise.jpeg',
            id='users_one',
        ),
    ],
)
@pytest.mark.usefixtures('reset_db')
@pytest.mark.asyncio
async def test_consume(
    message_value,
    monkeypatch,
    caplog,
    user,
    db_helper,
):
    caplog.set_level(logging.INFO)

    async def decompress_mock(message: str) -> str:
        return message

    monkeypatch.setattr(
        'app.external.kafka.decompress',
        decompress_mock,
    )

    monkeypatch.setattr(
        'app.db.db_helper.db_helper.session_factory',
        db_helper.session_factory,
    )

    message = Mock()
    message.key = user.id
    message.value = message_value

    await consume(ConsumerMock([message]))

    async with db_helper.session_factory() as session:
        founded_user = await session.get(User, user.id)

    assert f'user_id={user.id}' in caplog.text
    assert founded_user.is_verified
    assert founded_user.verification_vector
