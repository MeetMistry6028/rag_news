from functools import lru_cache
from rag.chain import RAGChain
from retrieval.retriever import Retriever, RetrievalMode
from config.settings import get_settings


@lru_cache()
def get_rag_chain() -> RAGChain:
    """
    Single shared RAGChain instance.
    lru_cache ensures the embedding model and LLM
    are loaded once, not on every request.
    """
    return RAGChain(mode=RetrievalMode.VECTOR)


@lru_cache()
def get_retriever() -> Retriever:
    return Retriever(mode=RetrievalMode.VECTOR)