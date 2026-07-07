import json
import time
import structlog
from pathlib import Path
from rag.chain import RAGChain

logger = structlog.get_logger(__name__)

QUERIES_PATH = Path(__file__).resolve().parent / "test_queries.json"


def score_answer_grounding(answer: str, chunks: list[dict]) -> float:
    """
    Simple grounding score: what fraction of sentences in the answer
    contain words that appear in the retrieved chunks.
    This is a lightweight proxy for faithfulness without an LLM judge.
    """
    if not answer or not chunks:
        return 0.0

    all_chunk_text = " ".join(c.get("text", "") for c in chunks).lower()
    chunk_words = set(all_chunk_text.split())

    sentences = [s.strip() for s in answer.split(".") if len(s.strip()) > 10]
    if not sentences:
        return 0.0

    grounded = 0
    for sentence in sentences:
        words = set(sentence.lower().split())
        overlap = words & chunk_words
        if len(overlap) / max(len(words), 1) > 0.3:
            grounded += 1

    return round(grounded / len(sentences), 4)


def run_answer_eval(top_k: int = 5) -> dict:
    """
    Run RAG answer evaluation over all test queries.
    """
    queries = load_queries()
    chain = RAGChain()

    results = []
    latencies = []

    for q in queries:
        start = time.perf_counter()
        result = chain.ask(q["question"], top_k=top_k)
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        latencies.append(latency_ms)

        grounding_score = score_answer_grounding(
            result["answer"],
            []
        )

        results.append({
            "id": q["id"],
            "question": q["question"],
            "answer_length": len(result["answer"]),
            "citations": len(result["citations"]),
            "fallback": result["fallback"],
            "grounding_score": grounding_score,
            "latency_ms": latency_ms,
        })

        logger.info(
            "Answer evaluated",
            id=q["id"],
            fallback=result["fallback"],
            citations=len(result["citations"]),
            latency_ms=latency_ms,
        )

    p50 = round(sorted(latencies)[len(latencies) // 2], 2)
    p95 = round(sorted(latencies)[int(len(latencies) * 0.95)], 2)
    avg_citations = round(sum(r["citations"] for r in results) / len(results), 2)
    fallback_rate = round(sum(1 for r in results if r["fallback"]) / len(results), 4)

    return {
        "queries": results,
        "summary": {
            "p50_latency_ms": p50,
            "p95_latency_ms": p95,
            "avg_citations_per_answer": avg_citations,
            "fallback_rate": fallback_rate,
            "total_queries": len(results),
        }
    }


def load_queries() -> list[dict]:
    with open(QUERIES_PATH) as f:
        return json.load(f)


if __name__ == "__main__":
    from config.logger import setup_logging
    setup_logging()
    report = run_answer_eval(top_k=5)

    print("\n=== ANSWER EVALUATION REPORT ===")
    print(f"Total queries: {report['summary']['total_queries']}")
    print(f"Avg citations per answer: {report['summary']['avg_citations_per_answer']}")
    print(f"Fallback rate: {report['summary']['fallback_rate']}")
    print(f"P50 latency: {report['summary']['p50_latency_ms']}ms")
    print(f"P95 latency: {report['summary']['p95_latency_ms']}ms")
    print("\nPer-query results:")
    for r in report["queries"]:
        print(f"  [{r['id']}] citations={r['citations']} fallback={r['fallback']} {r['latency_ms']}ms")