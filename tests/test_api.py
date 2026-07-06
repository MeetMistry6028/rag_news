import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app

client = TestClient(app)


def make_chunk(article_id="abc123", score=0.4):
    return {
        "article_id": article_id,
        "chunk_index": 0,
        "text": "Sample article text about Egypt and protests.",
        "highlights": "Egypt protests summary.",
        "score": score,
        "retrieval_method": "vector",
    }


def test_health_endpoint():
    with patch("api.routers.health.QdrantClient") as mock_client:
        mock_client.return_value.count.return_value = MagicMock(count=982)
        response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "embedding_model" in data
    assert "llm_model" in data


def test_search_endpoint():
    mock_retriever = MagicMock()
    mock_retriever.search.return_value = [make_chunk()]

    with patch("api.dependencies.get_retriever", return_value=mock_retriever):
        with patch("api.routers.search.get_retriever", return_value=mock_retriever):
            response = client.post("/api/search", json={"query": "Egypt protests", "top_k": 3})

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "Egypt protests"
    assert "results" in data
    assert "total" in data


def test_search_validation_too_short():
    response = client.post("/api/search", json={"query": "hi"})
    assert response.status_code == 422


def test_ask_endpoint():
    mock_chain = MagicMock()
    mock_chain.ask.return_value = {
        "answer": "Egypt is experiencing protests. [Article 1]",
        "citations": [{
            "citation_num": 1,
            "article_id": "abc123",
            "text_preview": "Egypt protests text...",
            "highlights": "Summary here.",
        }],
        "chunks_used": 3,
        "fallback": False,
    }

    with patch("api.dependencies.get_rag_chain", return_value=mock_chain):
        with patch("api.routers.ask.get_rag_chain", return_value=mock_chain):
            response = client.post("/api/ask", json={"question": "What is happening in Egypt?", "top_k": 5})

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] != ""
    assert data["fallback"] is False
    assert "citations" in data


def test_ask_validation_too_short():
    response = client.post("/api/ask", json={"question": "hi"})
    assert response.status_code == 422