import structlog
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)
from config.settings import get_settings

logger = structlog.get_logger(__name__)


class VectorStore:
    """
    Wraps Qdrant client with collection management
    and upsert logic.
    """

    def __init__(self):
        self.settings = get_settings()
        self.client = QdrantClient(
            host=self.settings.qdrant_host,
            port=self.settings.qdrant_port,
        )
        self.collection_name = self.settings.collection_name

    def create_collection_if_not_exists(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name in existing:
            logger.info("Collection already exists", name=self.collection_name)
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.settings.embedding_dimensions,
                distance=Distance.COSINE,
            ),
        )
        logger.info("Created collection", name=self.collection_name)

    def upsert(self, points: list[dict]):
        """
        Upsert a list of points into Qdrant.
        Each point must have: id, vector, payload.
        """
        if not points:
            return

        qdrant_points = [
            PointStruct(
                id=p["id"],
                vector=p["vector"],
                payload=p["payload"],
            )
            for p in points
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=qdrant_points,
        )
        logger.info("Upserted points", count=len(points))

    def count(self) -> int:
        result = self.client.count(collection_name=self.collection_name)
        return result.count