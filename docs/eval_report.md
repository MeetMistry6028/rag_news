# rag_news — Evaluation Report

**Generated:** 2026-07-07 11:06
**Dataset:** CNN/DailyMail (100 articles ingested)
**Embedding model:** all-MiniLM-L6-v2 (local)
**LLM:** llama3.2 via Ollama (local)

---

## Retrieval Metrics

| Metric | Value |
|--------|-------|
| Avg Precision@5 | 0.68 |
| P50 Latency | 33.2ms |
| P95 Latency | 234.54ms |
| Queries evaluated | 10 |

## Answer Generation Metrics

| Metric | Value |
|--------|-------|
| Avg citations per answer | 0.6 |
| Fallback rate | 0.0 |
| P50 Answer latency | 2344.76ms |
| P95 Answer latency | 12270.25ms |

## Per-Query Retrieval Results

| Query ID | Question | Precision@5 | Latency |
|----------|----------|-------------|---------|
| q1 | What is happening in Egypt?... | 1.0 | 234.54ms |
| q2 | What is ISIS doing in Iraq?... | 1.0 | 49.39ms |
| q3 | What are politicians saying about Obama?... | 1.0 | 42.03ms |
| q4 | What is happening in Syria?... | 1.0 | 25.29ms |
| q5 | What are the latest sports results?... | 0.6 | 40.09ms |
| q6 | What crimes have been reported recently?... | 0.4 | 31.55ms |
| q7 | What is happening with elections around ... | 0.8 | 16.3ms |
| q8 | What health issues are in the news?... | 0.2 | 33.2ms |
| q9 | What is happening with the economy?... | 0.0 | 28.64ms |
| q10 | What environmental issues are being disc... | 0.8 | 15.62ms |