from functools import lru_cache

import httpx
from fastapi import APIRouter, HTTPException

from app.agents.embedder import EmbedderAgent
from app.agents.orchestrator import Orchestrator
from app.core.schemas import ArticleRecord, ClassificationRequest, ClassificationResponse, TopicCreateRequest, TopicRecord
from app.db.chroma_store import ChromaStore


router = APIRouter()


@lru_cache
def get_store() -> ChromaStore:
    return ChromaStore()


@lru_cache
def get_embedder() -> EmbedderAgent:
    return EmbedderAgent()


@lru_cache
def get_orchestrator() -> Orchestrator:
    return Orchestrator()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/topics", response_model=TopicRecord)
async def create_topic(payload: TopicCreateRequest) -> TopicRecord:
    embedding = await get_embedder().run(f"{payload.name}. {payload.description}")
    return get_store().create_topic(payload.name, payload.description, embedding.vector)


@router.get("/topics", response_model=list[TopicRecord])
async def list_topics() -> list[TopicRecord]:
    return get_store().list_topics()


@router.post("/agent/classify", response_model=ClassificationResponse)
async def classify_article(payload: ClassificationRequest) -> ClassificationResponse:
    try:
        return await get_orchestrator().classify_url(str(payload.url))
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="Timeout while fetching or processing URL content.") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Target URL returned HTTP {exc.response.status_code}.",
        ) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"Failed to fetch target URL: {exc!s}") from exc
    except RuntimeError as exc:
        # Raised by Ollama client with a user-friendly message.
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/articles", response_model=list[ArticleRecord])
async def list_articles() -> list[ArticleRecord]:
    return get_store().list_articles()
