from eval.retrieval_eval import topic_precision
from eval.answer_eval import score_answer_grounding


def make_chunk(text: str, score: float = 0.4) -> dict:
    return {
        "article_id": "abc",
        "chunk_index": 0,
        "text": text,
        "highlights": "",
        "score": score,
        "retrieval_method": "vector",
    }


def test_topic_precision_perfect():
    chunks = [
        make_chunk("Egypt protests and Morsy supporters clashed"),
        make_chunk("Egypt election results announced"),
        make_chunk("Egypt military intervention"),
    ]
    score = topic_precision(chunks, ["egypt", "protest"], k=3)
    assert score == 1.0


def test_topic_precision_zero():
    chunks = [
        make_chunk("Football match results from yesterday"),
        make_chunk("Sports news from around the world"),
    ]
    score = topic_precision(chunks, ["egypt", "protest"], k=2)
    assert score == 0.0


def test_topic_precision_partial():
    chunks = [
        make_chunk("Egypt protests ongoing"),
        make_chunk("Football match results"),
    ]
    score = topic_precision(chunks, ["egypt"], k=2)
    assert score == 0.5


def test_topic_precision_empty_chunks():
    score = topic_precision([], ["egypt"], k=5)
    assert score == 0.0


def test_answer_grounding_good():
    chunks = [make_chunk("Egypt is experiencing protests and political unrest")]
    answer = "Egypt is experiencing protests. Political unrest continues."
    score = score_answer_grounding(answer, chunks)
    assert score > 0.0


def test_answer_grounding_empty():
    score = score_answer_grounding("", [])
    assert score == 0.0