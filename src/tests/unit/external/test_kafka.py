import logging
from unittest.mock import Mock

import brotli
import pytest
from aiokafka import AIOKafkaConsumer

from app.config import settings
from app.external.kafka import (
    consume,
    create_consumer,
    decompress,
    verificated_users,
)


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
    'messages, users',
    [
        pytest.param(
            [
                Mock(key=1, value='src/tests/images/image_for_vectorise.jpeg'),
            ],
            {1},
            id='users_one',
        ),
        pytest.param(
            [
                Mock(key=2, value='src/tests/images/image_for_vectorise.jpeg'),
            ],
            {2},
            id='users_two',
        ),
        pytest.param(
            [
                Mock(key=1, value='src/tests/images/image_for_vectorise.jpeg'),
                Mock(key=2, value='src/tests/images/image_for_vectorise.jpeg'),
            ],
            {1, 2},
            id='two_messages',
        ),
    ],
)
@pytest.mark.asyncio
async def test_consume(monkeypatch, clear, caplog, messages, users):
    caplog.set_level(logging.INFO)

    async def decompress_mock(message: str) -> str:
        return message

    monkeypatch.setattr(
        'app.external.kafka.decompress',
        decompress_mock,
    )

    await consume(ConsumerMock(messages))

    assert verificated_users == users
    for user_id in users:
        assert f'user_id={user_id}' in caplog.text
