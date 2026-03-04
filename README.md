# Contract Risk & Obligation Extractor (RAG)

Upload a contract (PDF/DOCX), index it into a built‑in lightweight vector store (pure Python + JSON, no external services), then extract:
- Obligations
- Deadlines
- Penalties / Liability

Then chat Q&A with citations.

⚠️ Not legal advice.

---

## 🛠 Tech Choices (Why)
- **Gradio** → fastest UI (upload + chat) with minimal frontend bugs.
- **FastAPI + LangServe** → exposes pipelines as microservice endpoints.
- **Simple JSON‑based vector store** → no native extensions or external dependencies, so ingestion never crashes.
- **Groq LLM** → used for chat responses (no OpenAI key required).  
- **Local hash embeddings** → mock embeddings for retrieval, so ingestion works offline.

---

## ⚙️ Setup (Windows)

### 1. Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

### 2. Install requirements
pip install -r requirements.txt
pip install -e .

### 3. Environment variables
GROQ_API_KEY=your_groq_key_here

### 4. Run the App
uvicorn contractqa.api.server:app --reload
