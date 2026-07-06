NO_CONTEXT_RESPONSE = (
    "I could not find relevant articles in the knowledge base to answer your question. "
    "Try rephrasing or asking about a different topic."
)

LOW_CONFIDENCE_THRESHOLD = 0.15


def should_fallback(chunks: list[dict]) -> bool:
    """
    Return True if retrieval results are too weak to generate a good answer.
    """
    if not chunks:
        return True
    best_score = max(c.get("score", 0) for c in chunks)
    return best_score < LOW_CONFIDENCE_THRESHOLD


def fallback_response() -> dict:
    return {
        "answer": NO_CONTEXT_RESPONSE,
        "citations": [],
        "chunks_used": 0,
        "fallback": True,
    }