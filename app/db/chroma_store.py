from __future__ import annotations

from typing import Any
from uuid import uuid4

import chromadb

from app.core.config import get_settings
from app.core.schemas import ArticleRecord, TopicRecord


class ChromaStore:
    def __init__(self) -> None:
        settings = get_settings()
        client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
        self.topics = client.get_or_create_collection(settings.chroma_topics_collection)
        self.articles = client.get_or_create_collection(settings.chroma_articles_collection)

    def create_topic(self, name: str, description: str, embedding: list[float]) -> TopicRecord:
        topic_id = str(uuid4())
        self.topics.add(
            ids=[topic_id],
            embeddings=[embedding],
            documents=[description],
            metadatas=[{"name": name, "description": description}],
        )
        return TopicRecord(id=topic_id, name=name, description=description)

    def list_topics(self) -> list[TopicRecord]:
        payload = self.topics.get(include=["metadatas"])
        result: list[TopicRecord] = []
        for idx, metadata in zip(payload["ids"], payload["metadatas"], strict=False):
            result.append(
                TopicRecord(
                    id=idx,
                    name=metadata["name"],
                    description=metadata["description"],
                )
            )
        return result

    def query_topics(self, embedding: list[float], limit: int = 5) -> list[dict[str, Any]]:
        result = self.topics.query(query_embeddings=[embedding], n_results=limit)
        ids = result.get("ids", [[]])[0]
        distances = result.get("distances", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        return [
            {
                "id": topic_id,
                "distance": distance,
                "name": metadata["name"],
                "description": metadata["description"],
            }
            for topic_id, distance, metadata in zip(ids, distances, metadatas, strict=False)
        ]

    def store_article(
        self,
        url: str,
        title: str | None,
        excerpt: str,
        topic: str,
        confidence: float,
        embedding: list[float],
    ) -> ArticleRecord:
        article_id = str(uuid4())
        self.articles.add(
            ids=[article_id],
            embeddings=[embedding],
            documents=[excerpt],
            metadatas=[
                {
                    "url": url,
                    "title": title,
                    "excerpt": excerpt,
                    "topic": topic,
                    "confidence": confidence,
                }
            ],
        )
        return ArticleRecord(
            id=article_id,
            url=url,
            title=title,
            excerpt=excerpt,
            topic=topic,
            confidence=confidence,
        )

    def list_articles(self) -> list[ArticleRecord]:
        payload = self.articles.get(include=["metadatas"])
        result: list[ArticleRecord] = []
        for idx, metadata in zip(payload["ids"], payload["metadatas"], strict=False):
            result.append(
                ArticleRecord(
                    id=idx,
                    url=metadata["url"],
                    title=metadata.get("title"),
                    excerpt=metadata["excerpt"],
                    topic=metadata["topic"],
                    confidence=float(metadata["confidence"]),
                )
            )
        return result
