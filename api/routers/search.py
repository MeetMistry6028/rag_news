import structlog
from fastapi import APIRouter, Depends, HTTPException
from api.schemas import SearchRequest, SearchResponse, SearchResult
from api.dependencies import get_retriever
from retrieval.retriever import Retriever

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post("/search", response_model=SearchResponse)
def search(request: SearchRequest, retriever: Retriever = Depends(get_retriever)):
    logger.info("Search request received", query=request.query)

    try:
        chunks = retriever.search(request.query, top_k=request.top_k)
    except Exception as e:
        logger.error("Search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Search failed. Please try again.")

    results = [
        SearchResult(
            article_id=c.get("article_id", ""),
            chunk_index=c.get("chunk_index", 0),
            text=c.get("text", ""),
            highlights=c.get("highlights", ""),
            score=c.get("score", 0.0),
            retrieval_method=c.get("retrieval_method", "vector"),
        )
        for c in chunks
    ]

    return SearchResponse(
        query=request.query,
        results=results,
        total=len(results),
    )