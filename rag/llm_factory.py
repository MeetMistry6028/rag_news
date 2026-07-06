from config.settings import get_settings


def get_llm():
    """
    Returns the right LLM based on config.
    Swap provider in config/default.yaml to switch models.
    """
    settings = get_settings()
    provider = settings.llm_provider

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            base_url=settings.llm_base_url,
        )

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.openai_api_key,
        )

    raise ValueError(f"Unknown LLM provider: {provider}")