import structlog
from retrieval.vector_retriever import VectorRetriever
from retrieval.bm25_retriever import BM25Retriever

logger = structlog.get_logger(__name__)


class HybridRetriever:
    """
    Combines vector and BM25 retrieval using
    Reciprocal Rank Fusion (RRF).

    RRF is a well-established rank fusion algorithm that
    doesn't require score normalization — it works purely
    on rank positions, making it robust when the two
    retrievers return different score scales.
    """

    def __init__(self, rrf_k: int = 60):
        self.vector_retriever = VectorRetriever()
        self.bm25_retriever = BM25Retriever()
        self.rrf_k = rrf_k

    def build_bm25_index(self, limit: int = 10000):
        self.bm25_retriever.build_index(limit=limit)

    def search(
        self,
        query: str,
        top_k: int = 5,
        filters: dict = None,
    ) -> list[dict]:
        """
        Run both retrievers, fuse results with RRF,
        return top_k deduplicated chunks.
        """
        vector_hits = self.vector_retriever.search(query, top_k=top_k * 2, filters=filters)
        bm25_hits = self.bm25_retriever.search(query, top_k=top_k * 2)

        fused = self._reciprocal_rank_fusion(vector_hits, bm25_hits, top_k=top_k)
        logger.info("Hybrid search complete", query=query, hits=len(fused))
        return fused

    def _reciprocal_rank_fusion(
        self,
        vector_hits: list[dict],
        bm25_hits: list[dict],
        top_k: int,
    ) -> list[dict]:
        scores: dict[str, float] = {}
        doc_map: dict[str, dict] = {}

        for rank, hit in enumerate(vector_hits):
            key = f"{hit['article_id']}_{hit['chunk_index']}"
            scores[key] = scores.get(key, 0) + 1 / (self.rrf_k + rank + 1)
            doc_map[key] = hit

        for rank, hit in enumerate(bm25_hits):
            key = f"{hit['article_id']}_{hit['chunk_index']}"
            scores[key] = scores.get(key, 0) + 1 / (self.rrf_k + rank + 1)
            if key not in doc_map:
                doc_map[key] = hit

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for key, rrf_score in ranked:
            doc = doc_map[key].copy()
            doc["score"] = round(rrf_score, 6)
            doc["retrieval_method"] = "hybrid"
            results.append(doc)

        return results