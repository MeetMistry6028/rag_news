import torch
import structlog
from sentence_transformers import SentenceTransformer

logger = structlog.get_logger(__name__)

MODEL_NAME = "all-MiniLM-L6-v2"


class LocalEmbedder:
    """
    Local embedding model using sentence-transformers.
    No API key needed. Runs entirely on your machine.

    Model: all-MiniLM-L6-v2
    - 384 dimensions (vs OpenAI's 1536)
    - Fast, good quality for retrieval tasks
    - ~90MB download on first use
    """

    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info("Loading local embedding model", model=MODEL_NAME)
        self.model = SentenceTransformer(MODEL_NAME, device=device)
        self.dimensions = 384

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(texts, show_progress_bar=False)
        logger.info("Embedded texts locally", count=len(texts))
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        embedding = self.model.encode([query], show_progress_bar=False)
        return embedding[0].tolist()