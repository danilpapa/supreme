from __future__ import annotations

import json

from app.agents.ollama_client import OllamaClient
from app.core.config import get_settings
from app.core.schemas import LLMClassification


CLASSIFIER_SYSTEM_PROMPT = """You are a topic classifier.
Return valid JSON with fields: topic, confidence, reason.
Confidence must be between 0 and 1.
Choose only one topic from the provided candidate list."""


class ClassifierAgent:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self.settings = get_settings()
        self.client = client or OllamaClient()

    async def run(self, article_text: str, topics: list[dict]) -> LLMClassification:
        user_prompt = (
            "Classify the article into the best topic.\n"
            f"Candidate topics:\n{json.dumps(topics, ensure_ascii=True)}\n"
            f"Article text:\n{article_text[:4000]}"
        )
        payload = await self.client.json_chat(
            model=self.settings.llm_model,
            system_prompt=CLASSIFIER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        return LLMClassification.model_validate(payload)
