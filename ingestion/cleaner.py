import re
import structlog

logger = structlog.get_logger(__name__)


def clean_article(text: str) -> str:
    """
    Clean a raw article string.

    Steps:
    - Strip leading/trailing whitespace
    - Collapse multiple newlines into one
    - Collapse multiple spaces into one
    - Remove non-printable characters
    """
    if not text or not isinstance(text, str):
        logger.warning("clean_article received empty or invalid input")
        return ""

    text = text.strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = "\n".join(line.strip() for line in text.splitlines())
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    return text.strip()


def clean_highlights(text: str) -> str:
    """
    Clean article highlights/summary text.
    Same pipeline as clean_article.
    """
    return clean_article(text)