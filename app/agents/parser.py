from __future__ import annotations

import ssl

from bs4 import BeautifulSoup
import httpx

from app.core.config import get_settings
from app.core.schemas import ParserResult


class ParserAgent:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def run(self, url: str) -> ParserResult:
        try:
            async with httpx.AsyncClient(timeout=self.settings.parser_timeout_seconds, follow_redirects=True) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": self.settings.parser_user_agent},
                )
                response.raise_for_status()
        except ssl.SSLError as exc:
            return await self._fallback_via_jina(url, exc)
        except httpx.HTTPError as exc:
            return await self._fallback_via_jina(url, exc)
        return self._parse_html(url, response.text)

    def _parse_html(self, url: str, html: str) -> ParserResult:
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.text.strip() if soup.title and soup.title.text else None
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = " ".join(soup.stripped_strings)
        excerpt = text[:500]
        return ParserResult(url=url, title=title, text=text, excerpt=excerpt)

    async def _fallback_via_jina(self, url: str, original_exc: Exception) -> ParserResult:
        fallback_url = f"{self.settings.parser_fallback_base_url}{url}"
        try:
            async with httpx.AsyncClient(timeout=self.settings.parser_timeout_seconds, follow_redirects=True) as client:
                response = await client.get(
                    fallback_url,
                    headers={"User-Agent": self.settings.parser_user_agent},
                )
                response.raise_for_status()
        except Exception as fallback_exc:
            raise RuntimeError(f"Failed to fetch URL due to SSL/network error: {url}") from fallback_exc

        body = response.text.strip()
        title = None
        first_line = body.splitlines()[0].strip() if body else ""
        if first_line:
            title = first_line[:200]
        if not body:
            raise RuntimeError(f"Failed to fetch URL due to SSL/network error: {url}") from original_exc
        return ParserResult(url=url, title=title, text=body, excerpt=body[:500])
