from dataclasses import dataclass


SYSTEM_PROMPT = """You are a knowledgeable news assistant.
Answer the user's question using ONLY the provided context from news articles.
If the context does not contain enough information to answer the question, say so clearly.
Do not make up information. Be concise and factual.
Always cite which article your answer comes from using [Article N] notation."""


USER_PROMPT_TEMPLATE = """Context from news articles:

{context}

Question: {question}

Answer based on the context above:"""


@dataclass
class PromptInput:
    question: str
    chunks: list[dict]


def build_context_string(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a numbered context block.
    Each chunk is labelled so the LLM can cite it.
    """
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[Article {i}]\n{chunk['text']}")
    return "\n\n".join(parts)


def build_prompt(question: str, chunks: list[dict]) -> tuple[str, str]:
    """
    Returns (system_prompt, user_prompt) tuple.
    """
    context = build_context_string(chunks)
    user_prompt = USER_PROMPT_TEMPLATE.format(
        context=context,
        question=question,
    )
    return SYSTEM_PROMPT, user_prompt