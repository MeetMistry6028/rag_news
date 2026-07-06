from config.settings import get_settings


def get_embedder():
    """
    Returns the right embedder based on config.
    Swap provider in config/default.yaml to switch models
    without touching any other code.
    """
    settings = get_settings()
    provider = settings.embedding_provider

    if provider == "local":
        from ingestion.local_embedder import LocalEmbedder
        return LocalEmbedder()

    if provider == "openai":
        from ingestion.embedder import Embedder
        return Embedder()

    raise ValueError(f"Unknown embedding provider: {provider}")