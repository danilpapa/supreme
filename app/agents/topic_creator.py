from app.agents.ollama_client import OllamaClient
from app.core.config import get_settings
from app.core.schemas import TopicSuggestion


TOPIC_CREATOR_SYSTEM_PROMPT = """You propose new topic names for articles.
Return valid JSON with fields: new_topic, reason.
Topic must be short, normalized, and reusable."""


class TopicCreatorAgent:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self.settings = get_settings()
        self.client = client or OllamaClient()

    async def run(self, article_text: str) -> TopicSuggestion:
        payload = await self.client.json_chat(
            model=self.settings.topic_creator_model,
            system_prompt=TOPIC_CREATOR_SYSTEM_PROMPT,
            user_prompt=f"Suggest a new topic for this article:\n{article_text[:4000]}",
        )
        return TopicSuggestion.model_validate(payload)
