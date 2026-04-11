from typing import Literal

from pydantic import BaseModel, Field, HttpUrl


class TopicCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=128)
    description: str = Field(min_length=5, max_length=512)


class TopicRecord(BaseModel):
    id: str
    name: str
    description: str


class ClassificationDecision(BaseModel):
    topic: str
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    mode: Literal["accepted", "validated", "new_topic"]
    suggested_new_topic: str | None = None


class ClassificationRequest(BaseModel):
    url: HttpUrl


class ClassificationResponse(BaseModel):
    url: HttpUrl
    title: str | None
    excerpt: str
    decision: ClassificationDecision


class ArticleRecord(BaseModel):
    id: str
    url: str
    title: str | None
    excerpt: str
    topic: str
    confidence: float


class ParserResult(BaseModel):
    url: str
    title: str | None
    text: str
    excerpt: str


class EmbeddingResult(BaseModel):
    vector: list[float]


class LLMClassification(BaseModel):
    topic: str
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str


class ValidationResult(BaseModel):
    valid: bool
    confidence_adjustment: float = Field(ge=-1.0, le=1.0)
    reason: str


class TopicSuggestion(BaseModel):
    new_topic: str = Field(min_length=2, max_length=128)
    reason: str
