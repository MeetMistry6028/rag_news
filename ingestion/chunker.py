import structlog
from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import get_settings

logger = structlog.get_logger(__name__)


@dataclass
class Chunk:
    article_id: str
    chunk_index: int
    text: str
    char_count: int
    word_count: int


def chunk_article(article_id: str, text: str) -> list[Chunk]:
    """
    Split a cleaned article into overlapping chunks.
    Uses RecursiveCharacterTextSplitter which tries to
    split on paragraphs first, then sentences, then words —
    preserving semantic boundaries wherever possible.
    """
    settings = get_settings()

    if not text or len(text.strip()) < 50:
        logger.warning("chunk_article received text too short to chunk", article_id=article_id)
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    raw_chunks = splitter.split_text(text)

    chunks = []
    for i, chunk_text in enumerate(raw_chunks):
        chunk_text = chunk_text.strip()
        if not chunk_text:
            continue
        chunks.append(Chunk(
            article_id=article_id,
            chunk_index=i,
            text=chunk_text,
            char_count=len(chunk_text),
            word_count=len(chunk_text.split()),
        ))

    logger.info("Chunked article", article_id=article_id, chunk_count=len(chunks))
    return chunks