import structlog
from fastapi import APIRouter
from qdrant_client import QdrantClient
from api.schemas import HealthResponse
from config.settings import get_settings

logger = structlog.get_logger(__name__)
router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check():
    settings = get_settings()

    vector_count = None
    try:
        client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
        vector_count = client.count(collection_name=settings.collection_name).count
    except Exception as e:
        logger.warning("Qdrant health check failed", error=str(e))

    return HealthResponse(
        status="ok",
        environment=settings.environment,
        vector_count=vector_count,
        embedding_model=settings.embedding_model,
        llm_model=settings.llm_model,
    )