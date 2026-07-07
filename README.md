# rag_news

An enterprise-grade Retrieval-Augmented Generation platform built over 300,000+ real-world CNN/DailyMail news articles. Designed to demonstrate production-level AI engineering practices.

![Demo](docs/demo.gif)

---

## What it does

- **Search mode** — semantic search over 300k+ articles using dense vector retrieval
- **Ask mode** — natural language Q&A with grounded answers and cited sources
- **Hybrid retrieval** — combines vector search and BM25 keyword search via Reciprocal Rank Fusion
- **No hallucination policy** — falls back gracefully when context is insufficient

---

## Measured performance

| Metric | Value |
|--------|-------|
| Avg Precision@5 | 0.68 |
| P50 retrieval latency | 33ms |
| P95 retrieval latency | 234ms |
| P50 answer latency | 2.3s |
| Fallback rate | 0.0 |
| Articles ingested | 300,000+ |

---

## Architecture

```
User → React UI → FastAPI → Retriever → Qdrant
                          ↓
                     LLM (Ollama/llama3.2)
                          ↓
                   Answer + Citations
```
---

## Tech stack

| Layer | Technology |
|-------|-----------|
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector store | Qdrant |
| Retrieval | Dense + BM25 hybrid with RRF |
| LLM | llama3.2 via Ollama |
| Backend | FastAPI + Python 3.11 |
| Frontend | React + Vite + Tailwind CSS |
| Containerisation | Docker + Docker Compose |

---

## Project structure
```
rag_news/
├── config/          # Settings, logging, YAML configs
├── ingestion/       # Cleaning, chunking, embedding pipeline
├── retrieval/       # Vector, BM25, hybrid retrieval
├── rag/             # Prompt building, LLM chain, citations
├── api/             # FastAPI routes and schemas
├── eval/            # Evaluation framework and metrics
├── frontend/        # React + Vite UI
├── tests/           # Unit and integration tests
├── notebooks/       # Data exploration
└── docs/            # Architecture docs and eval report
```

---

## Setup

### Prerequisites
- Python 3.11+
- Node.js 22+
- Docker Desktop
- Ollama with llama3.2

### Backend

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -r requirements.txt
cp .env.example .env        # add your config
docker run -d --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant
python ingest.py --csv data/train.csv --limit 1000
uvicorn api.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`

---

## Evaluation

```bash
python -m eval.retrieval_eval
python -m eval.answer_eval
python -m eval.report
```

See [docs/eval_report.md](docs/eval_report.md) for full results.

---

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check + vector count |
| `/api/search` | POST | Semantic search over articles |
| `/api/ask` | POST | RAG question answering |

Full docs at `http://localhost:8000/docs`