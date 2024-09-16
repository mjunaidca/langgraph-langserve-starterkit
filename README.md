# LangGraph LangServe Containers Development & Deployment

This is a starter kit to test and develop agentic systems using langgraph.

Run using docker or locally.

git clone ...

## Local Setup

```bash
cd server

#rename .env.example to .env and add OpenAI API Key
mv .env.example .env

poetry install

poetry run uvicorn app.main:app --host 0.0.0.0 --reload

open localhost:8000/docs
```

## Test Langserve Python Client

1. Open client folder.

2. Run the notebook

