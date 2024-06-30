from deepface import DeepFace


class FaceVerification:
    @staticmethod
    def image_to_vector(path: str):
        '''Функция превращает изображение в вектор.'''
        embedding_objs = DeepFace.represent(
            img_path=path, model_name="Facenet", enforce_detection=False
        )
        return embedding_objs[0]["embedding"]
