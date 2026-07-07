import json
from pathlib import Path
from datetime import datetime


def generate_report(retrieval_results: dict, answer_results: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        "# rag_news — Evaluation Report",
        f"\n**Generated:** {now}",
        f"**Dataset:** CNN/DailyMail (100 articles ingested)",
        f"**Embedding model:** all-MiniLM-L6-v2 (local)",
        f"**LLM:** llama3.2 via Ollama (local)",
        "",
        "---",
        "",
        "## Retrieval Metrics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Avg Precision@5 | {retrieval_results['summary']['avg_precision_at_k']} |",
        f"| P50 Latency | {retrieval_results['summary']['p50_latency_ms']}ms |",
        f"| P95 Latency | {retrieval_results['summary']['p95_latency_ms']}ms |",
        f"| Queries evaluated | {retrieval_results['summary']['total_queries']} |",
        "",
        "## Answer Generation Metrics",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Avg citations per answer | {answer_results['summary']['avg_citations_per_answer']} |",
        f"| Fallback rate | {answer_results['summary']['fallback_rate']} |",
        f"| P50 Answer latency | {answer_results['summary']['p50_latency_ms']}ms |",
        f"| P95 Answer latency | {answer_results['summary']['p95_latency_ms']}ms |",
        "",
        "## Per-Query Retrieval Results",
        "",
        "| Query ID | Question | Precision@5 | Latency |",
        "|----------|----------|-------------|---------|",
    ]

    for r in retrieval_results["queries"]:
        lines.append(
            f"| {r['id']} | {r['question'][:40]}... | {r['precision_at_k']} | {r['latency_ms']}ms |"
        )

    report = "\n".join(lines)

    output_path = Path("docs/eval_report.md")
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report)
    print(f"\nReport saved to {output_path}")
    return report


if __name__ == "__main__":
    from config.logger import setup_logging
    from eval.retrieval_eval import run_retrieval_eval
    from eval.answer_eval import run_answer_eval

    setup_logging()

    print("Running retrieval evaluation...")
    retrieval_results = run_retrieval_eval(top_k=5)

    print("\nRunning answer evaluation...")
    answer_results = run_answer_eval(top_k=5)

    report = generate_report(retrieval_results, answer_results)
    print("\n" + report)