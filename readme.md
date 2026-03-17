RAG API Assistant

RAG API Assistant is a production-style Retrieval-Augmented Generation system that answers developer questions using API documentation.

The system ingests multiple documentation formats, builds hybrid retrieval indexes, and generates grounded answers using large language models.

⸻

Features

• Hybrid retrieval (vector + BM25)
• Multi-query retrieval
• Cross-encoder reranking
• Parent-child document retrieval
• Contextual compression
• Token-budget context building
• LLM-based answer generation
• Streaming responses
• Retrieval evaluation framework
• RAG observability and tracing

⸻

System Architecture

The system follows a modular RAG pipeline:

User Query
│
▼
Query Understanding
│
▼
Hybrid Retrieval
│
▼
Cross-Encoder Reranking
│
▼
Parent Expansion
│
▼
Contextual Compression
│
▼
Token Budget Context Builder
│
▼
LLM Generation

Detailed architecture can be found in:

architecture.md

⸻

Project Structure

backend/
├ api/ FastAPI endpoints
├ config/ configuration and logging
├ evaluation/ evaluation tools
├ ingestion/ document ingestion pipeline
├ llm/ LLM clients and prompts
├ observability/ tracing and metrics
├ retrieval/ hybrid retrieval system
├ services/ service layer
└ vectorstore/ vector database interfaces

data/
├ raw_docs/ source documentation
├ processed_docs/ chunked documents
├ embeddings/ embedding vectors
├ bm25/ keyword index
└ index/ FAISS index

docker/ container configuration
scripts/ helper scripts
tests/ test cases

⸻

Installation

Clone the repository:

git clone https://github.com/areddy1805/rag_api_assistant.git
cd rag_api_assistant

Create virtual environment:

python -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

⸻

Running Document Ingestion

To build indexes from documentation:

python scripts/run_ingestion.py

This will:

• parse documents
• build parent-child chunks
• generate embeddings
• create vector and BM25 indexes

⸻

Running the API Server

Start the FastAPI server:

uvicorn backend.api.server:app --reload

Available endpoints:

POST /chat
POST /retrieve
GET /health
GET /metrics

⸻

Example Query

How do I create a Stripe payment intent?

Example response:

Endpoint: /v1/payment_intents
Method: POST

Create a PaymentIntent using the Stripe API. You can optionally set confirm=true
to create and confirm the PaymentIntent in a single request.

⸻

Evaluation

Generate evaluation dataset:

python -m backend.evaluation.generate_dataset

Run retrieval evaluation:

python -m backend.evaluation.evaluate_retrieval

Run generation evaluation:

python -m backend.evaluation.evaluate_generation

⸻

Observability

The system includes detailed RAG tracing.

Metrics logged:

query
rewrite
expansions
retrieved chunks
reranked chunks
context tokens
generation latency
grounding score
token usage

Logs are stored in:

logs/rag.log

⸻

Docker Deployment

Build container:

docker build -t rag-api-assistant .

Run with docker compose:

docker-compose up

⸻

Future Improvements

Potential enhancements:

• semantic caching
• adaptive retrieval depth
• query decomposition
• distributed indexing
• advanced reranking models

⸻

License

MIT License
:::
