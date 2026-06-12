from sentence_transformers import SentenceTransformer

from app.core.logger import logger


class EmbeddingService:

    def __init__(self):

        logger.info("loading_embedding_model")

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        logger.info("embedding_model_loaded")

    def generate_embedding(
        self,
        text: str,
    ):

        return self.model.encode(text).tolist()


embedding_service = EmbeddingService()
