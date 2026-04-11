# What to Say in the Report and Defense

## Why multi-agent

The task naturally splits into parsing, semantic representation, classification, validation, and topic growth. This is not artificial decomposition. It reduces errors and makes the system auditable.

## Why Qwen2.5 7B

- open model
- strong instruction following
- reliable JSON outputs
- realistic for local deployment

## Why embeddings first

Embedding similarity is cheaper and more deterministic than asking an LLM every time. The LLM is reserved for ambiguous cases.

## Why validator exists

It is a second control layer that reduces false positives and makes the design easier to defend as a true agentic system.

## Why Docker + Ollama + Chroma

This stack is easy to reproduce, easy to demo, and still respects isolation concerns.
