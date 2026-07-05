from ingestion.cleaner import clean_article
from ingestion.validator import validate_and_clean


def test_clean_article_basic():
    raw = "  Hello   world  \n\n\n  This is a test.  "
    result = clean_article(raw)
    assert result == "Hello world\n\nThis is a test."
    

def test_clean_article_empty():
    assert clean_article("") == ""
    assert clean_article(None) == ""


def test_clean_article_collapses_spaces():
    result = clean_article("too    many     spaces")
    assert "  " not in result


def test_validate_and_clean_valid():
    raw = {
        "id": "abc123",
        "article": "A" * 200,
        "highlights": "Short summary here."
    }
    result = validate_and_clean(raw)
    assert result is not None
    assert result.word_count > 0
    assert result.is_valid is True


def test_validate_and_clean_too_short():
    raw = {
        "id": "abc123",
        "article": "Too short",
        "highlights": "Summary"
    }
    result = validate_and_clean(raw)
    assert result is None