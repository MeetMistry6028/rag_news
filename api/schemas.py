from pydantic import BaseModel, Field
from typing import Optional


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


class Citation(BaseModel):
    citation_num: int
    article_id: str
    text_preview: str
    highlights: str


class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list[Citation]
    chunks_used: int
    fallback: bool


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)
    top_k: int = Field(default=5, ge=1, le=20)


class SearchResult(BaseModel):
    article_id: str
    chunk_index: int
    text: str
    highlights: str
    score: float
    retrieval_method: str


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
    total: int


class HealthResponse(BaseModel):
    status: str
    environment: str
    vector_count: Optional[int] = None
    embedding_model: str
    llm_model: str