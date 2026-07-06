from config.settings import get_settings

def test_settings_loads():
    settings = get_settings()
    assert settings.app_name == "rag_news"
    assert settings.embedding_model == "all-MiniLM-L6-v2"
    assert settings.chunk_size == 512
    print(f"\nEnvironment: {settings.environment}")
    print(f"Collection: {settings.collection_name}")