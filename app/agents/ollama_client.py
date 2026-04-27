from __future__ import annotations

import json
from typing import Any

import httpx

from app.core.config import get_settings


class OllamaClient:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def embed(self, text: str) -> list[float]:
        timeout = httpx.Timeout(
            connect=self.settings.request_timeout_seconds,
            write=self.settings.request_timeout_seconds,
            read=self.settings.embedding_timeout_seconds,
            pool=self.settings.request_timeout_seconds,
        )
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Prefer the current Ollama endpoint, but keep backward compatibility.
            primary_payload = {"model": self.settings.embedding_model, "input": text}
            fallback_payload = {"model": self.settings.embedding_model, "prompt": text}
            try:
                response = await client.post(
                    f"{self.settings.ollama_base_url}/api/embed",
                    json=primary_payload,
                )
                response.raise_for_status()
                payload = response.json()
                return self._extract_embedding(payload)
            except (httpx.HTTPStatusError, httpx.TimeoutException, KeyError, TypeError, ValueError):
                try:
                    response = await client.post(
                        f"{self.settings.ollama_base_url}/api/embeddings",
                        json=fallback_payload,
                    )
                except httpx.TimeoutException as exc:
                    raise RuntimeError(
                        "Ollama embeddings request timed out. "
                        f"model={self.settings.embedding_model}; "
                        f"read_timeout={self.settings.embedding_timeout_seconds}s"
                    ) from exc
                try:
                    response.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    details = response.text.strip()
                    raise RuntimeError(
                        "Ollama embeddings request failed. "
                        f"model={self.settings.embedding_model}; "
                        f"status={response.status_code}; body={details}"
                    ) from exc
                payload = response.json()
                return self._extract_embedding(payload)

    @staticmethod
    def _extract_embedding(payload: dict[str, Any]) -> list[float]:
        embedding = payload.get("embedding")
        if isinstance(embedding, list):
            return embedding
        embeddings = payload.get("embeddings")
        if (
            isinstance(embeddings, list)
            and embeddings
            and isinstance(embeddings[0], list)
        ):
            return embeddings[0]
        raise ValueError(f"Unexpected Ollama embedding payload: {payload}")

    async def json_chat(self, model: str, system_prompt: str, user_prompt: str) -> dict:
        timeout = httpx.Timeout(
            connect=self.settings.request_timeout_seconds,
            write=self.settings.request_timeout_seconds,
            read=self.settings.chat_timeout_seconds,
            pool=self.settings.request_timeout_seconds,
        )
        async with httpx.AsyncClient(timeout=timeout) as client:
            try:
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
            except httpx.TimeoutException as exc:
                raise RuntimeError(
                    "Ollama chat request timed out. "
                    f"model={model}; read_timeout={self.settings.chat_timeout_seconds}s"
                ) from exc
            if response.status_code == 404:
                return await self._json_generate_fallback(
                    client=client,
                    model=model,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )
            response.raise_for_status()
            payload = response.json()
        return json.loads(payload["message"]["content"])

    async def _json_generate_fallback(
        self,
        client: httpx.AsyncClient,
        model: str,
        system_prompt: str,
        user_prompt: str,
    ) -> dict:
        # Older Ollama versions may not expose /api/chat.
        prompt = (
            f"{system_prompt}\n\n"
            "Return ONLY valid JSON without markdown fences.\n\n"
            f"User request:\n{user_prompt}"
        )
        try:
            response = await client.post(
                f"{self.settings.ollama_base_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "format": "json",
                    "stream": False,
                },
            )
        except httpx.TimeoutException as exc:
            raise RuntimeError(
                "Ollama generate request timed out. "
                f"model={model}; read_timeout={self.settings.chat_timeout_seconds}s"
            ) from exc
        response.raise_for_status()
        payload = response.json()
        return json.loads(payload["response"])
