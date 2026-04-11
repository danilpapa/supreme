from fastapi import FastAPI

from app.api.routes import router
from app.observability.metrics import metrics_router


app = FastAPI(
    title="Multi-Agent Topic Classifier",
    version="0.1.0",
    description="A local-first multi-agent system for URL topic classification.",
)
app.include_router(router)
app.include_router(metrics_router)
