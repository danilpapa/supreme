from __future__ import annotations

import json

from app.agents.ollama_client import OllamaClient
from app.core.config import get_settings
from app.core.schemas import ValidationResult


VALIDATOR_SYSTEM_PROMPT = """You are a classification validator.
Return valid JSON with fields: valid, confidence_adjustment, reason.
Reject weak or mismatched classifications."""


class ValidatorAgent:
    def __init__(self, client: OllamaClient | None = None) -> None:
        self.settings = get_settings()
        self.client = client or OllamaClient()

    async def run(self, article_text: str, candidate_topic: str, confidence: float, reason: str) -> ValidationResult:
        user_prompt = (
            "Validate the proposed topic classification.\n"
            f"Classification:\n{json.dumps({'topic': candidate_topic, 'confidence': confidence, 'reason': reason})}\n"
            f"Article text:\n{article_text[:4000]}"
        )
        payload = await self.client.json_chat(
            model=self.settings.validator_model,
            system_prompt=VALIDATOR_SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )
        return ValidationResult.model_validate(payload)
