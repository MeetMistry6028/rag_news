import structlog
from ingestion.schemas import RawArticle, CleanedArticle
from ingestion.cleaner import clean_article, clean_highlights

logger = structlog.get_logger(__name__)


def validate_and_clean(raw: dict) -> CleanedArticle | None:
    """
    Takes a raw row dict from the CSV, validates it,
    cleans it, and returns a CleanedArticle.
    Returns None if the row is invalid.
    """
    try:
        raw_article = RawArticle(**raw)
    except Exception as e:
        logger.warning("Raw article failed validation", error=str(e))
        return None

    cleaned_text = clean_article(raw_article.article)
    cleaned_highlights = clean_highlights(raw_article.highlights)

    try:
        return CleanedArticle(
            id=raw_article.id,
            article=cleaned_text,
            highlights=cleaned_highlights,
            word_count=len(cleaned_text.split()),
            char_count=len(cleaned_text),
        )
    except Exception as e:
        logger.warning("Cleaned article failed validation", id=raw_article.id, error=str(e))
        return None