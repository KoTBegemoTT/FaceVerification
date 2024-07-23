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
def test_get_vector(test_client, path):
    response = test_client.get('/get_vector/', params={'path': path})

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) == 128
