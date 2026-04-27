from app.agents.ollama_client import OllamaClient
from app.core.config import get_settings
from app.core.schemas import EmbeddingResult


class EmbedderAgent:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self.client = client or OllamaClient()
        self.settings = get_settings()

    async def run(self, text: str) -> EmbeddingResult:
        # Prevent oversized payloads that exceed embedding model context window.
        clipped_text = text[: self.settings.embedding_max_chars]
        vector = await self.client.embed(clipped_text)
        return EmbeddingResult(vector=vector)
