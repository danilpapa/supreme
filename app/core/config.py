from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen2.5:7b-instruct"
    validator_model: str = "qwen2.5:7b-instruct"
    topic_creator_model: str = "qwen2.5:7b-instruct"
    embedding_model: str = "bge-m3"
    classifier_accept_threshold: float = 0.80
    classifier_review_threshold: float = 0.60
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_topics_collection: str = "topics"
    chroma_articles_collection: str = "articles"
    request_timeout_seconds: float = 25.0
    parser_timeout_seconds: float = 40.0
    embedding_timeout_seconds: float = 120.0
    chat_timeout_seconds: float = 90.0
    embedding_max_chars: int = 12000
    parser_fallback_base_url: str = "https://r.jina.ai/"
    parser_user_agent: str = (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
