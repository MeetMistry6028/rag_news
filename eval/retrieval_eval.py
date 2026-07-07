import json
import time
import structlog
from pathlib import Path
from retrieval.retriever import Retriever, RetrievalMode

logger = structlog.get_logger(__name__)

QUERIES_PATH = Path(__file__).resolve().parent / "test_queries.json"


def load_queries() -> list[dict]:
    with open(QUERIES_PATH) as f:
        return json.load(f)


def topic_precision(chunks: list[dict], expected_topics: list[str], k: int = 5) -> float:
    """
    Measures what fraction of top-k chunks contain
    at least one expected topic keyword.
    This is a proxy for Precision@K when we don't have
    ground truth article IDs.
    """
    if not chunks:
        return 0.0

    top_k = chunks[:k]
    hits = 0

    for chunk in top_k:
        text = chunk.get("text", "").lower()
        if any(topic.lower() in text for topic in expected_topics):
            hits += 1

    return round(hits / len(top_k), 4)


def run_retrieval_eval(top_k: int = 5) -> dict:
    """
    Run retrieval evaluation over all test queries.
    Returns per-query metrics and aggregate stats.
    """
    queries = load_queries()
    retriever = Retriever(mode=RetrievalMode.VECTOR)

    results = []
    latencies = []

    for q in queries:
        start = time.perf_counter()
        chunks = retriever.search(q["question"], top_k=top_k)
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        latencies.append(latency_ms)

        precision = topic_precision(chunks, q["expected_topics"], k=top_k)

        results.append({
            "id": q["id"],
            "question": q["question"],
            "precision_at_k": precision,
            "hits": len(chunks),
            "latency_ms": latency_ms,
        })

        logger.info(
            "Query evaluated",
            id=q["id"],
            precision=precision,
            latency_ms=latency_ms,
        )

    avg_precision = round(sum(r["precision_at_k"] for r in results) / len(results), 4)
    p50_latency = round(sorted(latencies)[len(latencies) // 2], 2)
    p95_latency = round(sorted(latencies)[int(len(latencies) * 0.95)], 2)

    return {
        "queries": results,
        "summary": {
            "avg_precision_at_k": avg_precision,
            "p50_latency_ms": p50_latency,
            "p95_latency_ms": p95_latency,
            "total_queries": len(results),
            "top_k": top_k,
        }
    }


if __name__ == "__main__":
    from config.logger import setup_logging
    setup_logging()
    report = run_retrieval_eval(top_k=5)

    print("\n=== RETRIEVAL EVALUATION REPORT ===")
    print(f"Total queries: {report['summary']['total_queries']}")
    print(f"Avg Precision@5: {report['summary']['avg_precision_at_k']}")
    print(f"P50 latency: {report['summary']['p50_latency_ms']}ms")
    print(f"P95 latency: {report['summary']['p95_latency_ms']}ms")
    print("\nPer-query results:")
    for r in report["queries"]:
        print(f"  [{r['id']}] P@5={r['precision_at_k']} | {r['latency_ms']}ms | {r['question'][:50]}")