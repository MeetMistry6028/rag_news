from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import yaml
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_yaml_config(env: str) -> dict:
    config = {}
    for fname in ["default.yaml", f"{env}.yaml"]:
        path = BASE_DIR / "config" / fname
        if path.exists():
            with open(path) as f:
                data = yaml.safe_load(f) or {}
                config = _deep_merge(config, data)
    return config


def _deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(result.get(k), dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "rag_news"
    app_version: str = "0.1.0"
    environment: str = "development"

    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")

    log_level: str = "INFO"
    log_format: str = "json"
    log_file: str = "logs/app.log"

    embedding_model: str = "text-embedding-3-small"
    embedding_batch_size: int = 100
    embedding_dimensions: int = 1536

    chunk_size: int = 512
    chunk_overlap: int = 64
    chunking_strategy: str = "recursive"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "rag_news_articles"

    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 1024

    retrieval_top_k: int = 5
    retrieval_score_threshold: float = 0.5
    enable_reranking: bool = False

    @classmethod
    def from_yaml(cls, env: str = "development") -> "Settings":
        yaml_config = _load_yaml_config(env)
        flat = _extract_known_fields(yaml_config)
        return cls(**flat)


def _extract_known_fields(yaml_config: dict) -> dict:
    """Pull only the values we need, using explicit key mapping."""
    c = yaml_config
    result = {}

    def get(d, *keys):
        for k in keys:
            if not isinstance(d, dict):
                return None
            d = d.get(k)
        return d

    mappings = {
        "app_name":               get(c, "app", "name"),
        "app_version":            get(c, "app", "version"),
        "environment":            get(c, "app", "environment"),
        "log_level":              get(c, "logging", "level"),
        "log_format":             get(c, "logging", "format"),
        "log_file":               get(c, "logging", "log_file"),
        "embedding_model":        get(c, "embedding", "model"),
        "embedding_batch_size":   get(c, "embedding", "batch_size"),
        "embedding_dimensions":   get(c, "embedding", "dimensions"),
        "chunking_strategy":      get(c, "chunking", "strategy"),
        "chunk_size":             get(c, "chunking", "chunk_size"),
        "chunk_overlap":          get(c, "chunking", "chunk_overlap"),
        "qdrant_host":            get(c, "vector_store", "host"),
        "qdrant_port":            get(c, "vector_store", "port"),
        "collection_name":        get(c, "vector_store", "collection_name"),
        "llm_model":              get(c, "llm", "model"),
        "llm_temperature":        get(c, "llm", "temperature"),
        "llm_max_tokens":         get(c, "llm", "max_tokens"),
        "retrieval_top_k":        get(c, "retrieval", "top_k"),
        "retrieval_score_threshold": get(c, "retrieval", "score_threshold"),
        "enable_reranking":       get(c, "retrieval", "enable_reranking"),
    }

    return {k: v for k, v in mappings.items() if v is not None}


@lru_cache()
def get_settings() -> Settings:
    env = os.getenv("ENVIRONMENT", "development")
    return Settings.from_yaml(env)