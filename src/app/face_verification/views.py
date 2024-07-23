from deepface import DeepFace  # type: ignore


def image_to_vector(path: str) -> list[float]:
    """Функция превращает изображение в вектор."""
    embedding_objs = DeepFace.represent(
        img_path=path, model_name='Facenet', enforce_detection=False,
    )
    return embedding_objs[0]['embedding']
