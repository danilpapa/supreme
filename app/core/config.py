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

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
