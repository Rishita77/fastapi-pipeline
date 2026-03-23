# Typed FastAPI Data Pipeline

A production-style data pipeline built with FastAPI and Pydantic.
Accepts individual records, batches, and CSV uploads — validates,
transforms, stores, and returns fully typed responses.

## Features
- End-to-end type safety with Pydantic v2
- Auto-generated Swagger/OpenAPI docs at /docs
- CSV file upload with row-level validation
- SQLite persistence via SQLAlchemy (swap to Postgres with one line)
- Dependency injection for database sessions
- Docker container support added to the app

## Quickstart
```bash
git clone https://github.com/YOUR_USERNAME/fastapi-pipeline
cd fastapi-pipeline
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Visit http://127.0.0.1:8000/docs to explore the API.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /ingest/record | Submit one sale record |
| POST | /ingest/batch | Submit a batch |
| POST | /ingest/upload | Upload CSV |
| GET | /results | List stored records |
| GET | /health | Health check |
