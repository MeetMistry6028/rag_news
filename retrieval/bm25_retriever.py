import structlog
import nltk
from rank_bm25 import BM25Okapi
from qdrant_client import QdrantClient
from config.settings import get_settings

logger = structlog.get_logger(__name__)


class BM25Retriever:
    """
    Keyword-based retrieval using BM25 over chunks
    fetched from Qdrant.

    BM25 complements vector search by handling exact
    keyword matches that semantic search can miss —
    e.g. names, codes, specific terms.
    """

    def __init__(self):
        self.settings = get_settings()
        self.client = QdrantClient(
            host=self.settings.qdrant_host,
            port=self.settings.qdrant_port,
        )
        self.collection_name = self.settings.collection_name
        self._corpus: list[dict] = []
        self._bm25 = None

    def build_index(self, limit: int = 10000):
        """
        Load chunks from Qdrant and build a BM25 index in memory.
        Call this once before searching.
        """
        logger.info("Building BM25 index...")

        results, _ = self.client.scroll(
            collection_name=self.collection_name,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        self._corpus = [
            {
                "article_id": r.payload.get("article_id"),
                "chunk_index": r.payload.get("chunk_index"),
                "text": r.payload.get("text"),
                "highlights": r.payload.get("highlights"),
            }
            for r in results
        ]

        tokenized = [
            nltk.word_tokenize(doc["text"].lower())
            for doc in self._corpus
        ]

        self._bm25 = BM25Okapi(tokenized)
        logger.info("BM25 index built", documents=len(self._corpus))

    def search(self, query: str, top_k: int = None) -> list[dict]:
        """
        Search the BM25 index for keyword matches.
        """
        if self._bm25 is None:
            raise RuntimeError("BM25 index not built. Call build_index() first.")

        top_k = top_k or self.settings.retrieval_top_k
        tokenized_query = nltk.word_tokenize(query.lower())
        scores = self._bm25.get_scores(tokenized_query)

        top_indices = sorted(
            range(len(scores)), key=lambda i: scores[i], reverse=True
        )[:top_k]

        hits = []
        for i in top_indices:
            if scores[i] > 0:
                hits.append({
                    **self._corpus[i],
                    "score": round(float(scores[i]), 4),
                    "retrieval_method": "bm25",
                })

        logger.info("BM25 search complete", query=query, hits=len(hits))
        return hits