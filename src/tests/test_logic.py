import pytest
from app.logic import FaceVerification


class TestFaceVerification:
    @pytest.mark.parametrize(
        "path",
        [
            "src/tests/images/image_for_vectorise.jpeg",
            "src/tests/images/image_for_vectorise2.png",
        ]
    )
    def test_image_to_vetor_convert(self, path):
        embedding = FaceVerification.image_to_vector(path)
        assert type(embedding) == list
        assert len(embedding) == 128

    @pytest.mark.parametrize(
        "path, error",
        [
            ("not_exist.jpg", ValueError),
            (10001, ValueError),
        ]
    )
    def test_image_to_vetor_fail(self, path, error):
        with pytest.raises(error):
            embedding = FaceVerification.image_to_vector(path)
