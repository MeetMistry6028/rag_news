# rag_news
<<<<<<< HEAD

An enterprise-grade Retrieval-Augmented Generation platform built on 300,000+ real-world news articles.

## Stack
- **Embeddings**: OpenAI text-embedding-3-small
- **Vector store**: Qdrant
- **LLM**: GPT-4o-mini via LangChain
- **Backend**: FastAPI
- **Frontend**: React + Vite + Tailwind

## Project structure
rag_news/
├── config/        # Settings, logging, YAML configs
├── ingestion/     # Cleaning, chunking, embedding pipeline
├── retrieval/     # Vector, BM25, hybrid retrieval
├── rag/           # Prompt building, chain, citations
├── api/           # FastAPI routes
├── eval/          # Evaluation framework
├── tests/         # Unit and integration tests
└── data/          # Raw data (gitignored)

## Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # add your OpenAI key

## Run
uvicorn api.main:app --reload
=======
>>>>>>> 11711fdc460bfacef9d8387f600176cbc08f6f88
