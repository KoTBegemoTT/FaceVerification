from app.logic import FaceVerification

def test_image_to_vetor_convert():
    embedding = FaceVerification.image_to_vector("src/tests/images/image_for_vectorise.jpeg")
    assert type(embedding) == list
    assert len(embedding) == 128
