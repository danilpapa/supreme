from __future__ import annotations

from bs4 import BeautifulSoup
import httpx

from app.core.config import get_settings
from app.core.schemas import ParserResult


class ParserAgent:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def run(self, url: str) -> ParserResult:
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.text.strip() if soup.title and soup.title.text else None
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = " ".join(soup.stripped_strings)
        excerpt = text[:500]
        return ParserResult(url=url, title=title, text=text, excerpt=excerpt)
