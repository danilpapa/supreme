from app.agents.ollama_client import OllamaClient
from app.core.schemas import EmbeddingResult


class EmbedderAgent:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self.client = client or OllamaClient()

    async def run(self, text: str) -> EmbeddingResult:
        vector = await self.client.embed(text)
        return EmbeddingResult(vector=vector)
