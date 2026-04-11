from __future__ import annotations

import json

import httpx

from app.core.config import get_settings


class OllamaClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def embed(self, text: str) -> list[float]:
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(
                f"{self.settings.ollama_base_url}/api/embeddings",
                json={"model": self.settings.embedding_model, "prompt": text},
            )
            response.raise_for_status()
            payload = response.json()
        return payload["embedding"]

    async def json_chat(self, model: str, system_prompt: str, user_prompt: str) -> dict:
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(
                f"{self.settings.ollama_base_url}/api/chat",
                json={
                    "model": model,
                    "format": "json",
                    "stream": False,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                },
            )
            response.raise_for_status()
            payload = response.json()
        return json.loads(payload["message"]["content"])
