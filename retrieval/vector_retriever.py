import structlog
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue, QueryRequest
from ingestion.embedder_factory import get_embedder
from config.settings import get_settings

logger = structlog.get_logger(__name__)


class VectorRetriever:
    """
    Retrieves semantically similar chunks from Qdrant
    using dense vector search.
    """

    def __init__(self):
        self.settings = get_settings()
        self.client = QdrantClient(
            host=self.settings.qdrant_host,
            port=self.settings.qdrant_port,
        )
        self.embedder = get_embedder()
        self.collection_name = self.settings.collection_name

    def search(
        self,
        query: str,
        top_k: int = None,
        filters: dict = None,
    ) -> list[dict]:
        """
        Embed the query and retrieve top_k most similar chunks.
        Optionally filter by metadata fields.
        """
        top_k = top_k or self.settings.retrieval_top_k
        query_vector = self.embedder.embed_query(query)

        qdrant_filter = self._build_filter(filters) if filters else None

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
            query_filter=qdrant_filter,
            with_payload=True,
            score_threshold=self.settings.retrieval_score_threshold,
        ).points

        hits = []
        for r in results:
            hits.append({
                "article_id": r.payload.get("article_id"),
                "chunk_index": r.payload.get("chunk_index"),
                "text": r.payload.get("text"),
                "highlights": r.payload.get("highlights"),
                "score": round(r.score, 4),
                "retrieval_method": "vector",
            })

        logger.info("Vector search complete", query=query, hits=len(hits))
        return hits

    def _build_filter(self, filters: dict) -> Filter:
        conditions = []
        for field, value in filters.items():
            conditions.append(
                FieldCondition(key=field, match=MatchValue(value=value))
            )
        return Filter(must=conditions)