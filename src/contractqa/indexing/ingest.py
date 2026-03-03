import shutil
from pathlib import Path
from contractqa.config import settings
from contractqa.loaders import load_any
from contractqa.indexing.splitter import get_splitter
from contractqa.indexing.vectorstore import clear_store, get_vectorstore


def ingest_contract(file_path: str) -> dict:
    settings.ensure_dirs()

    src = Path(file_path)
    if not src.exists():
        raise FileNotFoundError(str(src))

    dst = settings.uploads_dir / src.name
    shutil.copy2(src, dst)

    # Simplest MVP: one contract at a time
    print("[DEBUG] ingest_contract: clearing store directory")
    clear_store()
    print("[DEBUG] ingest_contract: creating vectorstore instance")
    vectorstore = get_vectorstore()

    raw_docs = load_any(str(dst))
    print(f"[DEBUG] ingest_contract: loaded {len(raw_docs)} raw documents")
    chunks = get_splitter().split_documents(raw_docs)
    print(f"[DEBUG] ingest_contract: split into {len(chunks)} chunks")

    try:
        print("[DEBUG] ingest_contract: adding documents to vectorstore")
        vectorstore.add_documents(chunks)
        print("[DEBUG] ingest_contract: add_documents completed successfully")
    except Exception as e:
        print("[ERROR] ingest_contract: exception during add_documents", e)
        raise

    return {
        "uploaded_file": dst.name,
        "pages_loaded": len(raw_docs),
        "chunks_indexed": len(chunks),
        "vector_db": "Chroma (local folder)",
        "storage_dir": str(settings.chroma_dir),
    }