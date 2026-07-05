from ingestion.deduplicator import Deduplicator


def test_first_article_not_duplicate():
    d = Deduplicator()
    assert d.is_duplicate("some article text") is False


def test_same_article_is_duplicate():
    d = Deduplicator()
    d.is_duplicate("some article text")
    assert d.is_duplicate("some article text") is True


def test_different_articles_not_duplicate():
    d = Deduplicator()
    assert d.is_duplicate("article one") is False
    assert d.is_duplicate("article two") is False


def test_seen_count():
    d = Deduplicator()
    d.is_duplicate("a")
    d.is_duplicate("b")
    d.is_duplicate("a")
    assert d.seen_count == 2