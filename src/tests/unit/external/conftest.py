import pytest

from app.external.kafka import verificated_users


@pytest.fixture
def clear() -> None:
    verificated_users.clear()
