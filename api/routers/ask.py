import structlog
from fastapi import APIRouter, Depends, HTTPException
from api.schemas import AskRequest, AskResponse, Citation
from api.dependencies import get_rag_chain
from rag.chain import RAGChain

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest, chain: RAGChain = Depends(get_rag_chain)):
    logger.info("Ask request received", question=request.question)

    try:
        result = chain.ask(request.question, top_k=request.top_k)
    except Exception as e:
        logger.error("RAG chain failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate answer.")

    citations = [
        Citation(
            citation_num=c.get("citation_num", 0),
            article_id=c.get("article_id", ""),
            text_preview=c.get("text_preview", ""),
            highlights=c.get("highlights", ""),
        )
        for c in result.get("citations", [])
    ]

    return AskResponse(
        question=request.question,
        answer=result["answer"],
        citations=citations,
        chunks_used=result["chunks_used"],
        fallback=result["fallback"],
    )