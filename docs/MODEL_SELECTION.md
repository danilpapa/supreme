# Model Selection

## Local LLM runtimes compared

1. `Ollama`
   Best operational simplicity. Strong choice for local demos and student projects.
2. `llama.cpp`
   Great for constrained hardware and GGUF models, but less convenient as a service stack.
3. `vLLM`
   Best throughput on serious GPU servers. Operationally heavier than needed here.
4. `LocalAI`
   Flexible compatibility layer, but less opinionated and usually less smooth for a focused local stack.

## Candidate open models

1. `Qwen2.5 7B Instruct`
   Best all-around balance for reasoning, instruction following, and structured JSON.
2. `Llama 3.1 8B Instruct`
   Strong baseline, but often a bit less disciplined in tool-like JSON tasks.
3. `Mistral 7B Instruct`
   Lightweight and good latency, but weaker on ambiguous classification than Qwen in many practical setups.

## Recommended choice

Choose `Qwen2.5 7B Instruct` as the main agent model.

## Why this is optimal for your task

- handles short reasoning chains well
- produces stable schema-shaped output
- runs locally on accessible hardware compared to larger models
- good enough to act as both classifier and validator in the first version

## Embedding model

Choose `bge-m3` if available in your local setup.

Why:
- strong multilingual coverage
- useful if articles or topic names mix Russian and English
- simple one-model baseline for semantic memory
