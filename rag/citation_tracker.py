import re
import structlog

logger = structlog.get_logger(__name__)


def extract_citations(answer: str, chunks: list[dict]) -> list[dict]:
    """
    Find [Article N] references in the answer and map them
    back to the original chunks with their article IDs.
    """
    cited = []
    pattern = re.compile(r"\[Article (\d+)\]")
    matches = pattern.findall(answer)

    seen = set()
    for match in matches:
        idx = int(match) - 1
        if 0 <= idx < len(chunks) and idx not in seen:
            seen.add(idx)
            chunk = chunks[idx]
            cited.append({
                "citation_num": int(match),
                "article_id": chunk.get("article_id"),
                "text_preview": chunk.get("text", "")[:150],
                "highlights": chunk.get("highlights", ""),
            })

    logger.info("Citations extracted", count=len(cited))
    return cited