📄 Project Overview & Technology Rationale

**Contract Risk & Obligation Extractor (RAG)** is a self‑contained Python application that lets users upload a PDF/DOCX contract, index it into a local vector database, extract key clauses (obligations, deadlines, penalties), and then ask natural language questions with context‑aware, cited answers.

---

🧩 Core Architecture
- **Python 3.10+** – ubiquitous language, excellent library ecosystem, and ease of rapid prototyping.
- **FastAPI** – lightweight, async web framework with automatic OpenAPI docs; ideal for exposing the ingestion/extraction/chat endpoints.
- **Gradio** – provides an instant web UI (file upload, chat, buttons) with no front‑end coding; dramatically reduces development time.

---

📚 Vector Storage & Embeddings
- **Simple JSON‑backed store** (formerly “Chroma directory”) – the original Chroma dependency caused random crashes on Windows; replaced by a tiny pure Python store that:
  - Uses deterministic hash embeddings (no API calls, no downloads).
  - Persists to `store.json` so data survives restarts.
  - Eliminates native code, avoiding platform‑specific bugs.
- **LocalHashEmbeddings** – custom hash vector generator ensures repeatable vectors and zero external requirements.  
  (Originally OpenAI embeddings → then Hugging Face inference API → now entirely offline.)

---

📤 Document Handling
- **PyMuPDF (fitz)** and **python‑docx** – lightweight, widely used libraries for reading PDF and DOCX content.
- **LangChain text splitting** – the `langchain-text-splitters` package is used to chunk documents into manageable pieces for indexing and retrieval.

---

🤖 QA / LLM
- **LangServe** (via `langchain_core.runnables`) – wraps answer/extract functions as server‑side runnables and provides playgrounds.
- **Groq LLM API** – used for chat responses with citations.  
  - No OpenAI key required.  
  - Supports models like `llama-3.1-70b-instruct`.  
  - Embeddings and vector store remain local, so ingestion is fully offline.

---

🛠 Supporting Libraries
- **python‑dotenv** – auto loads `.env` for convenient API key management during development.
- **langchain & related packages** – used for document handling, splitting, and messaging abstractions.
- **uvicorn** – ASGI server recommended for FastAPI.
- **sse‑starlette** – needed by Gradio for live updates.
- **Gradio/FastAPI/Uvicorn combo** – gives you both an API and a web UI with just a few lines.

---

🎯 Why This Stack Works
- ✅ **No external dependencies for core flow** – ingestion and indexing never call out to the network.
- ✅ **Minimal installation hassle** – one `pip install -r requirements.txt` and you’re ready.
- ✅ **Robust on Windows** – replaced problematic native code with pure Python.
- ✅ **Extensible** – swapping the chat model, adding encryption, or upgrading the store is easy due to clean abstractions.
- ✅ **Fast development & demo‑ready** – Gradio UI lets non‑technical users play immediately.
