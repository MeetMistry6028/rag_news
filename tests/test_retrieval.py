from unittest.mock import MagicMock, patch
from retrieval.vector_retriever import VectorRetriever
from retrieval.bm25_retriever import BM25Retriever
from retrieval.hybrid_retriever import HybridRetriever
from retrieval.metadata_filter import MetadataFilter


def make_hit(article_id, chunk_index, score, method="vector"):
    return {
        "article_id": article_id,
        "chunk_index": chunk_index,
        "text": f"Sample text for {article_id}",
        "highlights": "Summary.",
        "score": score,
        "retrieval_method": method,
    }


def test_metadata_filter_builds_correctly():
    f = MetadataFilter()
    f.add("article_id", "abc123")
    assert f.to_dict() == {"article_id": "abc123"}
    assert not f.is_empty()


def test_metadata_filter_empty():
    f = MetadataFilter()
    assert f.is_empty()


def test_rrf_fusion_deduplicates():
    hybrid = HybridRetriever.__new__(HybridRetriever)
    hybrid.rrf_k = 60

    vector_hits = [make_hit("a1", 0, 0.9), make_hit("a2", 0, 0.8)]
    bm25_hits = [make_hit("a1", 0, 5.0, "bm25"), make_hit("a3", 0, 4.0, "bm25")]

    result = hybrid._reciprocal_rank_fusion(vector_hits, bm25_hits, top_k=5)
    ids = [(r["article_id"], r["chunk_index"]) for r in result]

    assert len(set(ids)) == len(ids), "Duplicates found in fused results"
    assert ("a1", 0) in ids


def test_rrf_fusion_top_k_respected():
    hybrid = HybridRetriever.__new__(HybridRetriever)
    hybrid.rrf_k = 60

    vector_hits = [make_hit(f"a{i}", 0, 0.9 - i * 0.1) for i in range(5)]
    bm25_hits = [make_hit(f"b{i}", 0, 5.0 - i, "bm25") for i in range(5)]

    result = hybrid._reciprocal_rank_fusion(vector_hits, bm25_hits, top_k=3)
    assert len(result) == 3


def test_bm25_search_returns_results():
    retriever = BM25Retriever.__new__(BM25Retriever)
    retriever.settings = MagicMock()
    retriever.settings.retrieval_top_k = 5

    retriever._corpus = [
        {"article_id": "a1", "chunk_index": 0, "text": "climate change global warming", "highlights": ""},
        {"article_id": "a2", "chunk_index": 0, "text": "football world cup sports", "highlights": ""},
        {"article_id": "a3", "chunk_index": 0, "text": "climate policy environment", "highlights": ""},
    ]

    import nltk
    tokenized = [nltk.word_tokenize(d["text"].lower()) for d in retriever._corpus]
    from rank_bm25 import BM25Okapi
    retriever._bm25 = BM25Okapi(tokenized)

    results = retriever.search("climate change", top_k=2)
    assert len(results) <= 2
    assert all(r["score"] > 0 for r in results)
    assert results[0]["article_id"] in ["a1", "a3"]