# Memory Design

## Chosen approach

Chroma stores two semantic memories:

- `topics`
  - topic name
  - topic description
  - topic embedding
- `articles`
  - URL
  - title
  - excerpt
  - assigned topic
  - confidence
  - article embedding

## Why Chroma

- fast semantic search
- simple HTTP deployment
- enough for course-scale RAG and memory

## Alternatives

1. PostgreSQL + pgvector
   Better transactional guarantees, but more setup.
2. Weaviate
   Strong feature set, heavier to operate.
3. FAISS only
   Fast but lacks convenient metadata persistence by itself.

## Limits of current design

- no long-term episodic memory for agent conversations
- no versioning for changed topics
- no hybrid lexical search yet

## How to improve later

- add reranking over top-k topic candidates
- store article summaries separately from raw excerpts
- combine vector search with BM25 for improved recall
