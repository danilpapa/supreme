# API Contract

## `POST /topics`

Adds a confirmed topic into semantic memory.

Request:
```json
{
  "name": "programming",
  "description": "Software development, algorithms, tooling, testing, and backend/frontend engineering."
}
```

## `GET /topics`

Returns all known topics.

## `POST /agent/classify`

Runs the full multi-agent pipeline.

Request:
```json
{
  "url": "https://example.com/article"
}
```

Response when topic is known:
```json
{
  "url": "https://example.com/article",
  "title": "Article title",
  "excerpt": "Short article excerpt",
  "decision": {
    "topic": "programming",
    "confidence": 0.86,
    "reason": "Accepted by embedding similarity threshold.",
    "mode": "accepted",
    "suggested_new_topic": null
  }
}
```

Response when topic is not known:
```json
{
  "url": "https://example.com/article",
  "title": "Article title",
  "excerpt": "Short article excerpt",
  "decision": {
    "topic": "nutrition",
    "confidence": 0.4,
    "reason": "Similarity too low. The article is about meal planning and dietary choices.",
    "mode": "new_topic",
    "suggested_new_topic": "nutrition"
  }
}
```

## `GET /articles`

Returns already processed article records.

## `GET /metrics`

Prometheus scrape target.
