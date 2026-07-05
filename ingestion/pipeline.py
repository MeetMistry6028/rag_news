import uuid
import structlog
import pandas as pd
from ingestion.cleaner import clean_article
from ingestion.validator import validate_and_clean
from ingestion.chunker import chunk_article
from ingestion.embedder import Embedder
from ingestion.deduplicator import Deduplicator
from ingestion.vector_store import VectorStore

logger = structlog.get_logger(__name__)


def generate_point_id(article_id: str, chunk_index: int) -> str:
    """Generate a deterministic UUID from article_id + chunk_index."""
    namespace = uuid.UUID("12345678-1234-5678-1234-567812345678")
    return str(uuid.uuid5(namespace, f"{article_id}_{chunk_index}"))


def run_pipeline(csv_path: str, limit: int = None):
    """
    Full ingestion pipeline:
    load → validate → clean → deduplicate → chunk → embed → upsert
    """
    logger.info("Starting ingestion pipeline", csv_path=csv_path, limit=limit)

    embedder = Embedder()
    deduplicator = Deduplicator()
    vector_store = VectorStore()

    vector_store.create_collection_if_not_exists()

    df = pd.read_csv(csv_path, nrows=limit)
    logger.info("Loaded CSV", rows=len(df))

    stats = {"processed": 0, "skipped": 0, "chunks_total": 0}

    for _, row in df.iterrows():
        cleaned = validate_and_clean(row.to_dict())
        if cleaned is None:
            stats["skipped"] += 1
            continue

        if deduplicator.is_duplicate(cleaned.article):
            stats["skipped"] += 1
            continue

        chunks = chunk_article(cleaned.id, cleaned.article)
        if not chunks:
            stats["skipped"] += 1
            continue

        texts = [c.text for c in chunks]
        vectors = embedder.embed_texts(texts)

        points = []
        for chunk, vector in zip(chunks, vectors):
            points.append({
                "id": generate_point_id(chunk.article_id, chunk.chunk_index),
                "vector": vector,
                "payload": {
                    "article_id": chunk.article_id,
                    "chunk_index": chunk.chunk_index,
                    "text": chunk.text,
                    "word_count": chunk.word_count,
                    "highlights": cleaned.highlights,
                },
            })

        vector_store.upsert(points)
        stats["processed"] += 1
        stats["chunks_total"] += len(chunks)

    logger.info("Pipeline complete", **stats)
    logger.info("Total vectors in store", count=vector_store.count())
    return stats