# Evals

Run evaluations against the local stack after loading a gold dataset.

Suggested flow:

1. Start `docker compose up`.
2. Pull models into Ollama.
3. Seed topics.
4. Run repeated classification on the gold dataset.
5. Compare accuracy, consistency, latency, and fallback rates.
