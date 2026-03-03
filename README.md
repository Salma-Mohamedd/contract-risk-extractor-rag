# Contract Risk & Obligation Extractor (RAG)

Upload a contract (PDF/DOCX), index it into a built-in lightweight vector store (pure Python + JSON, no external services), then extract:
- Obligations
- Deadlines
- Penalties / Liability

Then chat Q&A with citations.

## Tech choices (why)
- Gradio: fastest UI (upload + chat) with minimal frontend bugs.
- FastAPI + LangServe: exposes pipelines as microservice endpoints.
- Simple JSON-based vector store: no native extensions or external dependencies, so ingestion never crashes.
- OpenAI: used only for ChatGPT responses; you can also run without an API key if you switch LLMs.

## Setup (Windows)
Create venv on D, install requirements:
- `python -m venv .venv`
- `.\.venv\Scripts\Activate.ps1`
- `pip install -r requirements.txt`
- `pip install -e .`

Set your API key if using OpenAI chat model (optional for testing):

- PowerShell: `$env:OPENAI_API_KEY="YOUR_KEY"`

The embedding flow is entirely local and does **not** require any API key.
Run:
- `uvicorn contractqa.api.server:app --reload`

Open:
- UI: http://127.0.0.1:8000/
- Docs: http://127.0.0.1:8000/docs
- LangServe:
  - POST /api/chat/invoke
  - POST /api/extract/invoke

Not legal advice.