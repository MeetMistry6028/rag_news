import structlog
from langchain_core.messages import SystemMessage, HumanMessage
from rag.llm_factory import get_llm
from rag.prompt_builder import build_prompt
from rag.citation_tracker import extract_citations
from rag.fallback_handler import should_fallback, fallback_response
from retrieval.retriever import Retriever, RetrievalMode

logger = structlog.get_logger(__name__)


class RAGChain:
    """
    Orchestrates the full RAG pipeline:
    query → retrieve → prompt → generate → cite
    """

    def __init__(self, mode: RetrievalMode = RetrievalMode.VECTOR):
        self.retriever = Retriever(mode=mode)
        self.llm = get_llm()

    def ask(self, question: str, top_k: int = 5) -> dict:
        """
        Ask a question, retrieve context, generate a grounded answer.
        Returns answer, citations, and the chunks used.
        """
        logger.info("RAG chain invoked", question=question)

        chunks = self.retriever.search(question, top_k=top_k)

        if should_fallback(chunks):
            logger.warning("Fallback triggered", question=question)
            return fallback_response()

        system_prompt, user_prompt = build_prompt(question, chunks)

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        response = self.llm.invoke(messages)
        answer = response.content

        citations = extract_citations(answer, chunks)

        logger.info("RAG chain complete", citations=len(citations))

        return {
            "answer": answer,
            "citations": citations,
            "chunks_used": len(chunks),
            "fallback": False,
        }
    