from __future__ import annotations

from dataclasses import dataclass

from app.agents.classifier import ClassifierAgent
from app.agents.embedder import EmbedderAgent
from app.agents.parser import ParserAgent
from app.agents.topic_creator import TopicCreatorAgent
from app.agents.validator import ValidatorAgent
from app.core.config import get_settings
from app.core.schemas import ClassificationDecision, ClassificationResponse, TopicSuggestion
from app.observability.metrics import AGENT_LATENCY_SECONDS, CLASSIFICATION_COUNTER, FALLBACK_COUNTER
from app.db.chroma_store import ChromaStore


@dataclass
class OrchestratorDependencies:
    parser: ParserAgent
    embedder: EmbedderAgent
    classifier: ClassifierAgent
    validator: ValidatorAgent
    topic_creator: TopicCreatorAgent
    store: ChromaStore


class Orchestrator:
    def __init__(self, deps: OrchestratorDependencies | None = None) -> None:
        self.settings = get_settings()
        self.deps = deps or OrchestratorDependencies(
            parser=ParserAgent(),
            embedder=EmbedderAgent(),
            classifier=ClassifierAgent(),
            validator=ValidatorAgent(),
            topic_creator=TopicCreatorAgent(),
            store=ChromaStore(),
        )

    async def classify_url(self, url: str) -> ClassificationResponse:
        with AGENT_LATENCY_SECONDS.labels("parser").time():
            parsed = await self.deps.parser.run(url)
        with AGENT_LATENCY_SECONDS.labels("embedder").time():
            article_embedding = await self.deps.embedder.run(parsed.text)
        topic_candidates = self.deps.store.query_topics(article_embedding.vector, limit=5)
        if not topic_candidates:
            suggestion = await self._safe_topic_suggestion(parsed.text)
            decision = ClassificationDecision(
                topic=suggestion.new_topic,
                confidence=0.5,
                reason=suggestion.reason,
                mode="new_topic",
                suggested_new_topic=suggestion.new_topic,
            )
            self.deps.store.store_article(
                url=str(url),
                title=parsed.title,
                excerpt=parsed.excerpt,
                topic=decision.topic,
                confidence=decision.confidence,
                embedding=article_embedding.vector,
            )
            CLASSIFICATION_COUNTER.labels(decision.mode).inc()
            return ClassificationResponse(url=url, title=parsed.title, excerpt=parsed.excerpt, decision=decision)

        best_candidate = topic_candidates[0]
        similarity = max(0.0, 1.0 - float(best_candidate["distance"]))

        if similarity >= self.settings.classifier_accept_threshold:
            decision = ClassificationDecision(
                topic=best_candidate["name"],
                confidence=round(similarity, 3),
                reason="Accepted by embedding similarity threshold.",
                mode="accepted",
            )
        elif similarity >= self.settings.classifier_review_threshold:
            FALLBACK_COUNTER.labels("validator").inc()
            try:
                with AGENT_LATENCY_SECONDS.labels("classifier").time():
                    llm_decision = await self.deps.classifier.run(parsed.text, topic_candidates)
                with AGENT_LATENCY_SECONDS.labels("validator").time():
                    validation = await self.deps.validator.run(
                        article_text=parsed.text,
                        candidate_topic=llm_decision.topic,
                        confidence=llm_decision.confidence,
                        reason=llm_decision.reason,
                    )
            except Exception as exc:
                decision = ClassificationDecision(
                    topic=best_candidate["name"],
                    confidence=round(similarity, 3),
                    reason=f"LLM fallback unavailable; used top embedding match. Details: {self._compact_error(exc)}",
                    mode="accepted",
                )
                self.deps.store.store_article(
                    url=str(url),
                    title=parsed.title,
                    excerpt=parsed.excerpt,
                    topic=decision.topic,
                    confidence=decision.confidence,
                    embedding=article_embedding.vector,
                )
                CLASSIFICATION_COUNTER.labels(decision.mode).inc()
                return ClassificationResponse(url=url, title=parsed.title, excerpt=parsed.excerpt, decision=decision)
            adjusted_confidence = min(1.0, max(0.0, llm_decision.confidence + validation.confidence_adjustment))
            if validation.valid:
                decision = ClassificationDecision(
                    topic=llm_decision.topic,
                    confidence=adjusted_confidence,
                    reason=f"{llm_decision.reason} Validator: {validation.reason}",
                    mode="validated",
                )
            else:
                FALLBACK_COUNTER.labels("topic_creator").inc()
                suggestion = await self._safe_topic_suggestion(parsed.text)
                decision = ClassificationDecision(
                    topic=suggestion.new_topic,
                    confidence=0.45,
                    reason=f"Validator rejected candidate. {suggestion.reason}",
                    mode="new_topic",
                    suggested_new_topic=suggestion.new_topic,
                )
        else:
            FALLBACK_COUNTER.labels("topic_creator").inc()
            suggestion = await self._safe_topic_suggestion(parsed.text)
            decision = ClassificationDecision(
                topic=suggestion.new_topic,
                confidence=0.4,
                reason=f"Similarity too low ({similarity:.3f}). {suggestion.reason}",
                mode="new_topic",
                suggested_new_topic=suggestion.new_topic,
            )

        self.deps.store.store_article(
            url=str(url),
            title=parsed.title,
            excerpt=parsed.excerpt,
            topic=decision.topic,
            confidence=decision.confidence,
            embedding=article_embedding.vector,
        )
        CLASSIFICATION_COUNTER.labels(decision.mode).inc()
        return ClassificationResponse(url=url, title=parsed.title, excerpt=parsed.excerpt, decision=decision)

    async def _safe_topic_suggestion(self, article_text: str) -> TopicSuggestion:
        try:
            with AGENT_LATENCY_SECONDS.labels("topic_creator").time():
                return await self.deps.topic_creator.run(article_text)
        except Exception as exc:
            return TopicSuggestion(
                new_topic="general",
                reason=(
                    "Topic creator unavailable; fallback topic assigned. "
                    f"Details: {self._compact_error(exc)}"
                ),
            )

    @staticmethod
    def _compact_error(exc: Exception) -> str:
        message = str(exc).strip().replace("\n", " ")
        return message[:180]
