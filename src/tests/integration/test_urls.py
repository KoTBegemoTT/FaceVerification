import pytest
from fastapi import status


@pytest.mark.parametrize(
    'path',
    [
        pytest.param(
            'src/tests/images/image_for_vectorise.jpeg',
            id='jpeg_image',
        ),
        pytest.param(
            'src/tests/images/image_for_vectorise_2.png',
            id='png_image',
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_vector(ac, path):
    response = await ac.get('/get_vector/', params={'path': path})

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 128


@pytest.mark.asyncio
async def test_check_ready(ac):
    response = await ac.get('/healthz/ready/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()
