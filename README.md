# Multi-Agent Topic Classifier

Local-first multi-agent system that classifies article URLs into user-defined topics.

## Recommended stack

- Backend: `Python + FastAPI`
- Local LLM runtime: `Ollama`
- Reasoning model: `Qwen2.5 7B Instruct`
- Embeddings: `bge-m3`
- Vector memory: `Chroma`
- Observability: `Prometheus + Grafana + Loguru`

## Quick start

1. `docker compose up --build`
2. Pull models into Ollama:
   - `ollama pull qwen2.5:7b-instruct`
   - `ollama pull bge-m3`
3. Seed topics through `POST /topics`
4. Classify a URL through `POST /agent/classify`
5. If the response returns `mode="new_topic"`, review `suggested_new_topic` and confirm it with `POST /topics`

## Main endpoints

- `POST /topics`
- `GET /topics`
- `POST /agent/classify`
- `GET /articles`
- `GET /metrics`

## Why this design

The system is agentic because each step has an explicit role, boundary, and evaluation path:

- parser
- embedder
- classifier
- validator
- topic creator
- orchestrator
