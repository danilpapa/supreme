# Multi-Agent Architecture

## Agents

1. `Orchestrator`
   Regular Python control plane. It decides which agents to call and when.
2. `ParserAgent`
   Downloads a URL and extracts readable text.
3. `EmbedderAgent`
   Converts article text and topic descriptions into vectors.
4. `ClassifierAgent`
   Uses LLM reasoning when embedding confidence is not enough.
5. `ValidatorAgent`
   Performs a second-pass quality check to reduce false positives.
6. `TopicCreatorAgent`
   Suggests a new topic when the article does not fit existing ones.

## Why this is a real multi-agent system

- Each agent has a narrow cognitive role.
- Agents can fail differently and be evaluated independently.
- The pipeline is transparent enough for oral defense.

## Recommended open model

- Main model: `Qwen2.5 7B Instruct`
- Why:
  - strong reasoning per VRAM compared to many 7B-8B models
  - stable JSON output for agent contracts
  - easy local deployment via Ollama
- Embeddings: `bge-m3`

## Model/runtime comparison

### Local runtimes

1. `Ollama`
   Best for fast setup, local demos, and course work.
2. `llama.cpp`
   Best when you need tight control or very small edge deployments.
3. `vLLM`
   Best for higher-throughput GPU inference, but heavier operationally.
4. `TGI`
   Good production runtime, weaker fit for a lightweight student project.

Chosen default: `Ollama` because it is the easiest to run, defend, and reproduce locally.

## Endpoint design

- `POST /topics`
  Add a new topic with description.
- `GET /topics`
  List known topics.
- `POST /agent/classify`
  Main endpoint. Accepts a URL and runs the full orchestration flow. If no topic fits, it returns `suggested_new_topic` without auto-approving it.
- `GET /articles`
  Retrieve already classified articles.
- `GET /metrics`
  Prometheus metrics for latency, fallback rates, and outcomes.
