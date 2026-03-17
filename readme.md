# RAG API Assistant

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-green)
![RAG](https://img.shields.io/badge/AI-RAG-purple)
![Vector DB](https://img.shields.io/badge/vector%20db-FAISS-orange)
![LLM](https://img.shields.io/badge/LLM-Qwen2.5-red)
![Architecture](https://img.shields.io/badge/architecture-hybrid%20RAG-blue)
![Evaluation](https://img.shields.io/badge/evaluation-retrieval%20%2B%20generation-green)
![Observability](https://img.shields.io/badge/observability-RAG%20tracing-orange)
![License](https://img.shields.io/badge/license-MIT-yellow)

Production-style **Retrieval-Augmented Generation (RAG)** system that answers developer questions using API documentation.

The system ingests heterogeneous documentation sources, builds hybrid retrieval indexes, and generates **grounded answers** using LLMs.

This project demonstrates a **complete applied-AI architecture** including:

• document ingestion  
• hybrid retrieval  
• reranking  
• context compression  
• grounded generation  
• observability  
• evaluation framework

---

Add a “System Demo / Example Trace” section near the top of the README. This shows the system actually runs and exposes the internal RAG pipeline. It signals engineering maturity more than badges alone.

---

Section to add to README

## Example RAG Pipeline Trace

Example query:

How do I create a Stripe payment intent?

Pipeline execution:

[QUERY] create stripe payment intent

[TIMING]
rewrite 0.39s
expansion 0.44s
retrieval 0.29s
rerank 1.69s
compression 0.87s
generation 9.80s

[RETRIEVED]
[400, 84, 375, 294, 104, 295, 306]

[RERANKED]
[295, 302, 294]

[CONTEXT TOKENS]
482

[GROUNDING SCORE]
0.68

Final answer:

Endpoint: /v1/payment_intents
Method: POST

Create a PaymentIntent using the Stripe API.
You can optionally set confirm=true to create and confirm the PaymentIntent in a single request.

---

# Architecture Overview

```text
User Query
   │
   ▼
Query Understanding
(rewrite + expansion + entity extraction)
   │
   ▼
Hybrid Retrieval
(vector + BM25 + endpoint search)
   │
   ▼
Reciprocal Rank Fusion
   │
   ▼
Cross Encoder Reranking
   │
   ▼
Parent Document Expansion
   │
   ▼
Contextual Compression
   │
   ▼
Token Budget Context Builder
   │
   ▼
LLM Generation
   │
   ▼
Grounding Validation
   │
   ▼
Final Answer

Full architecture details:

architecture.md

---

## Benchmark Results

| Metric | Score |
|------|------|
Retrieval Recall@3 | 0.84 |
Generation Score | 4.0 / 5 |
Context Tokens | ~480 |
End-to-End Latency | ~13s |


---

Key Capabilities

Hybrid Retrieval

The system combines multiple retrieval signals:

Retrieval Method	Purpose
Vector Search	semantic understanding
BM25 Search	keyword / identifier search
Endpoint Search	API endpoint matching
Metadata Filtering	service-specific routing

Vector search uses:

BAAI/bge-small-en-v1.5

Vector index:

FAISS


---

Multi-Query Retrieval

User queries are expanded into multiple semantic variants to improve recall.

Example

User Query
How do I create a Stripe payment intent?

Expanded Queries
create stripe payment intent
generate stripe payment intent
create a new stripe payment intent

This significantly improves retrieval performance.

---

Cross Encoder Reranking

Retrieved candidates are reranked using a cross encoder.

Model

BAAI/bge-reranker-base

The reranker scores

(query, document)

pairs directly, improving ranking quality.

---

Parent-Child Document Retrieval

Documents are chunked into

Parent Documents
Child Chunks

Retrieval occurs on child chunks for precision.

Then the parent document is restored for full context.

---

Contextual Compression

Parent documents can exceed token limits.

Compression uses a sentence-level relevance model to keep only the most relevant sentences.

Benefits

• reduces prompt size
• preserves semantic relevance
• improves generation accuracy

---

Token Budget Context Builder

Strict token limits are enforced before generation.

MAX_CONTEXT_TOKENS
MAX_CHUNK_TOKENS

This prevents prompt overflow and keeps generation stable.

---

Grounded Generation

Final answers are generated using retrieved context.

Models used

Model	Purpose
Qwen2.5 3B	query rewrite and expansion
Qwen2.5 7B	answer generation

Streaming responses are supported.

---

Observability

The system includes full RAG observability.

Captured metrics

query
rewrite
expansions
retrieved chunks
reranked chunks
context tokens
generation latency
token usage
grounding score

Example logs

[QUERY] create stripe payment intent
[TIMING] retrieval=0.21s
[RERANKED] [295, 302, 294]
[CONTEXT TOKENS] 482
[GROUNDING] score=0.68

Logs stored in

logs/rag.log


---

Evaluation Framework

The repository includes tools for evaluating retrieval and generation quality.

Retrieval Metrics

Chunk Recall@K
Parent Recall@K

Generation Metrics

LLM Judge Score
Grounding Score

Evaluation scripts

generate_dataset.py
evaluate_retrieval.py
evaluate_generation.py
analyze_retrieval_failures.py

Example evaluation

Retrieval Recall@3: 0.84
Generation Score: 4.0 / 5


---

Document Ingestion Pipeline

Supported sources

• HTML documentation
• Markdown documentation
• OpenAPI specifications
• PDF documents

Pipeline

Raw Docs
   │
   ▼
Loader Router
   │
   ▼
Parsing
   │
   ▼
Parent-Child Chunking
   │
   ▼
Embedding Generation
   │
   ▼
Index Construction

Output artifacts

data/
 ├ processed_docs/
 ├ embeddings/
 ├ bm25/
 └ index/

---

## RAG Techniques Implemented

| Technique | Implemented |
|-----------|-------------|
Hybrid Retrieval | ✓ |
Multi Query Retrieval | ✓ |
Cross Encoder Reranking | ✓ |
Parent Document Retrieval | ✓ |
Contextual Compression | ✓ |
Grounding Validation | ✓ |
Observability Tracing | ✓ |
Evaluation Framework | ✓ |
Semantic Cache | ✓ |
Query Decomposition | planned |

---

Project Structure

backend/
├ api/
├ config/
├ evaluation/
├ ingestion/
├ llm/
├ observability/
├ retrieval/
├ services/
└ vectorstore/

data/
├ raw_docs/
├ processed_docs/
├ embeddings/
├ bm25/
└ index/

docker/
scripts/
tests/


---

Installation

Clone repository

git clone https://github.com/areddy1805/rag_api_assistant.git
cd rag_api_assistant

Create environment

python -m venv .venv
source .venv/bin/activate

Install dependencies

pip install -r requirements.txt


---

Build Retrieval Index

python scripts/run_ingestion.py

This will

• parse documents
• create chunks
• generate embeddings
• build FAISS index
• build BM25 index

---

Run API Server

uvicorn backend.api.server:app --reload

Endpoints

POST /chat
POST /retrieve
GET /health
GET /metrics


---

Example Query

How do I create a Stripe payment intent?

Example response

Endpoint: /v1/payment_intents
Method: POST

Create a PaymentIntent using the Stripe API.
You can optionally set confirm=true to create and confirm the PaymentIntent in a single request.


---

Docker Deployment

Build container

docker build -t rag-api-assistant .

Run

docker-compose up


---

Future Improvements

• semantic caching
• adaptive retrieval depth
• stronger reranking models
• query decomposition
• distributed indexing
• advanced evaluation metrics

---

License

MIT License
```
