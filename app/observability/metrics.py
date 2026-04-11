from fastapi import APIRouter, Response
from prometheus_client import Counter, Histogram, generate_latest


AGENT_LATENCY_SECONDS = Histogram(
    "agent_latency_seconds",
    "Latency by agent stage",
    ["agent"],
)
CLASSIFICATION_COUNTER = Counter(
    "classification_total",
    "Classification outcomes",
    ["mode"],
)
FALLBACK_COUNTER = Counter(
    "fallback_total",
    "Fallback path usage",
    ["target"],
)

metrics_router = APIRouter()


@metrics_router.get("/metrics")
async def metrics() -> Response:
    return Response(generate_latest(), media_type="text/plain; version=0.0.4")
