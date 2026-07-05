from ingestion.chunker import chunk_article


def test_chunk_article_basic():
    text = "This is a sentence. " * 100
    chunks = chunk_article("test-id", text)
    assert len(chunks) > 1
    for chunk in chunks:
        assert chunk.article_id == "test-id"
        assert len(chunk.text) > 0
        assert chunk.word_count > 0


def test_chunk_article_too_short():
    chunks = chunk_article("test-id", "Too short")
    assert chunks == []


def test_chunk_article_empty():
    chunks = chunk_article("test-id", "")
    assert chunks == []


def test_chunk_indices_are_sequential():
    text = "Word " * 500
    chunks = chunk_article("test-id", text)
    indices = [c.chunk_index for c in chunks]
    assert indices == list(range(len(chunks)))