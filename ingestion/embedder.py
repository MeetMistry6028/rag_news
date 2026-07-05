import time
import structlog
from openai import OpenAI
from config.settings import get_settings

logger = structlog.get_logger(__name__)


class Embedder:
    """
    Wraps OpenAI's embedding API with batching and retry logic.
    Designed so the embedding model can be swapped without
    changing any downstream code.
    """

    def __init__(self):
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.openai_api_key)
        self.model = self.settings.embedding_model
        self.batch_size = self.settings.embedding_batch_size

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Embed a list of texts in batches.
        Returns a list of embedding vectors in the same order as input.
        """
        if not texts:
            return []

        all_embeddings = []

        for i in range(0, len(texts), self.batch_size):
            batch = texts[i: i + self.batch_size]
            embeddings = self._embed_batch_with_retry(batch)
            all_embeddings.extend(embeddings)
            logger.info("Embedded batch", batch_num=i // self.batch_size + 1, size=len(batch))

        return all_embeddings

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query string for retrieval."""
        result = self._embed_batch_with_retry([query])
        return result[0]

    def _embed_batch_with_retry(self, texts: list[str], retries: int = 3) -> list[list[float]]:
        for attempt in range(retries):
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=texts,
                )
                return [item.embedding for item in response.data]
            except Exception as e:
                logger.warning("Embedding attempt failed", attempt=attempt + 1, error=str(e))
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    raise