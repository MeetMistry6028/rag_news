from rag.prompt_builder import build_prompt, build_context_string
from rag.citation_tracker import extract_citations
from rag.fallback_handler import should_fallback, fallback_response


def make_chunk(article_id, text, score=0.5):
    return {
        "article_id": article_id,
        "chunk_index": 0,
        "text": text,
        "highlights": "summary",
        "score": score,
    }


def test_build_context_string():
    chunks = [make_chunk("a1", "Text about climate."), make_chunk("a2", "Text about football.")]
    context = build_context_string(chunks)
    assert "[Article 1]" in context
    assert "[Article 2]" in context
    assert "Text about climate." in context


def test_build_prompt_returns_tuple():
    chunks = [make_chunk("a1", "Some article text here.")]
    system, user = build_prompt("What happened?", chunks)
    assert len(system) > 0
    assert "What happened?" in user
    assert "[Article 1]" in user


def test_extract_citations_finds_references():
    chunks = [
        make_chunk("article-1", "Climate change text."),
        make_chunk("article-2", "Football text."),
    ]
    answer = "Climate is changing [Article 1]. Football is popular [Article 2]."
    citations = extract_citations(answer, chunks)
    assert len(citations) == 2
    assert citations[0]["article_id"] == "article-1"
    assert citations[1]["article_id"] == "article-2"


def test_extract_citations_handles_missing_reference():
    chunks = [make_chunk("article-1", "Some text.")]
    answer = "No citations here."
    citations = extract_citations(answer, chunks)
    assert citations == []


def test_should_fallback_empty_chunks():
    assert should_fallback([]) is True


def test_should_fallback_low_scores():
    chunks = [make_chunk("a1", "text", score=0.05)]
    assert should_fallback(chunks) is True


def test_should_fallback_good_scores():
    chunks = [make_chunk("a1", "text", score=0.4)]
    assert should_fallback(chunks) is False


def test_fallback_response_structure():
    result = fallback_response()
    assert result["fallback"] is True
    assert result["citations"] == []
    assert len(result["answer"]) > 0