from app.agents.orchestrator import Orchestrator, OrchestratorDependencies
from app.core.schemas import EmbeddingResult, LLMClassification, ParserResult, TopicSuggestion, ValidationResult


class FakeParser:
    async def run(self, url: str) -> ParserResult:
        return ParserResult(url=url, title="Title", text="Python unit tests and clean code", excerpt="Python unit tests")


class FakeEmbedder:
    async def run(self, text: str) -> EmbeddingResult:
        return EmbeddingResult(vector=[1.0, 0.0, 0.0])


class FakeClassifier:
    async def run(self, article_text: str, topics: list[dict]) -> LLMClassification:
        return LLMClassification(topic="programming", confidence=0.72, reason="Matches programming articles.")


class FakeValidator:
    async def run(self, article_text: str, candidate_topic: str, confidence: float, reason: str) -> ValidationResult:
        return ValidationResult(valid=True, confidence_adjustment=0.1, reason="Looks correct.")


class FakeTopicCreator:
    async def run(self, article_text: str) -> TopicSuggestion:
        return TopicSuggestion(new_topic="new topic", reason="Out of domain.")


class FakeStore:
    def __init__(self) -> None:
        self.articles = []
        self.created_topics = []

    def query_topics(self, embedding: list[float], limit: int = 5) -> list[dict]:
        return [{"id": "1", "distance": 0.35, "name": "programming", "description": "Software development"}]

    def create_topic(self, name: str, description: str, embedding: list[float]):
        self.created_topics.append(name)
        return type("Topic", (), {"name": name})()

    def store_article(self, **kwargs):
        self.articles.append(kwargs)
        return kwargs


async def test_orchestrator_borderline_path():
    deps = OrchestratorDependencies(
        parser=FakeParser(),
        embedder=FakeEmbedder(),
        classifier=FakeClassifier(),
        validator=FakeValidator(),
        topic_creator=FakeTopicCreator(),
        store=FakeStore(),
    )
    orchestrator = Orchestrator(deps=deps)
    result = await orchestrator.classify_url("https://example.com")
    assert result.decision.topic == "programming"
    assert result.decision.mode == "validated"
    assert len(deps.store.articles) == 1
