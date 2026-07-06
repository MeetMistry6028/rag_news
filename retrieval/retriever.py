import structlog
from enum import Enum
from retrieval.vector_retriever import VectorRetriever
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.metadata_filter import MetadataFilter

logger = structlog.get_logger(__name__)


class RetrievalMode(str, Enum):
    VECTOR = "vector"
    HYBRID = "hybrid"


class Retriever:
    """
    Unified retrieval interface.
    Callers pick a mode; this class routes to the right retriever.
    """

    def __init__(self, mode: RetrievalMode = RetrievalMode.HYBRID):
        self.mode = mode
        self._vector = VectorRetriever()
        self._hybrid = None

        if mode == RetrievalMode.HYBRID:
            self._hybrid = HybridRetriever()

    def build_index(self, limit: int = 10000):
        """Only needed for hybrid mode (builds BM25 index)."""
        if self._hybrid:
            self._hybrid.build_bm25_index(limit=limit)

    def search(
        self,
        query: str,
        top_k: int = 5,
        metadata_filter: MetadataFilter = None,
    ) -> list[dict]:
        filters = metadata_filter.to_dict() if metadata_filter and not metadata_filter.is_empty() else None

        if self.mode == RetrievalMode.VECTOR:
            return self._vector.search(query, top_k=top_k, filters=filters)

        if self.mode == RetrievalMode.HYBRID:
            return self._hybrid.search(query, top_k=top_k, filters=filters)

        raise ValueError(f"Unknown retrieval mode: {self.mode}")