from deepface import DeepFace  # type: ignore


class FaceVerification:
    """Класс предоставляющий возможности для верификации изображений."""

    @staticmethod
    def image_to_vector(path: str):
        """Функция превращает изображение в вектор."""
        embedding_objs = DeepFace.represent(
            img_path=path, model_name='Facenet', enforce_detection=False,
        )
        return embedding_objs[0]['embedding']
