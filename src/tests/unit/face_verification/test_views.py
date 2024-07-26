import pytest

from app.face_verification.views import image_to_vector


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
async def test_image_to_vetor_convert(path):
    embedding = await image_to_vector(path)

    assert isinstance(embedding, list)
    assert len(embedding) == 128


@pytest.mark.parametrize(
    'path, error',
    [
        pytest.param('not_exist.jpg', ValueError, id='not_exist'),
        pytest.param(10001, ValueError, id='wrong_path_type'),
    ],
)
@pytest.mark.asyncio
async def test_image_to_vetor_fail(path, error):
    with pytest.raises(error):
        await image_to_vector(path)
