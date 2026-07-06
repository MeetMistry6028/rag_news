import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.logger import setup_logging
from config.settings import get_settings
from api.routers import health, search, ask

setup_logging()
logger = structlog.get_logger(__name__)
settings = get_settings()

app = FastAPI(
    title="rag_news API",
    description="Enterprise RAG platform over CNN/DailyMail articles",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(ask.router, prefix="/api", tags=["ask"])


@app.on_event("startup")
async def startup():
    logger.info("rag_news API starting up", environment=settings.environment)


@app.on_event("shutdown")
async def shutdown():
    logger.info("rag_news API shutting down")