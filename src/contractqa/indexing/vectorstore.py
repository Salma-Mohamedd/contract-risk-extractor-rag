import os
import shutil
import json
from pathlib import Path
from typing import List, Tuple
from langchain_core.documents import Document
from contractqa.config import settings

# ---- embeddings provider (unchanged) ----

def get_embeddings():
    # diagnostic marker: indicate which get_embeddings version is executing
    print("[DEBUG] get_embeddings called - using local hash embeddings")

    class LocalHashEmbeddings:
        def __init__(self, dim: int = 128):
            self.dim = dim

        def _hash_vector(self, text: str) -> list[float]:
            h = abs(hash(text))
            vec = []
            for i in range(self.dim):
                vec.append(float((h >> (i * 8)) & 0xFF) / 255.0)
            return vec

        def embed_documents(self, texts: list[str]) -> list[list[float]]:
            return [self._hash_vector(t) for t in texts]

        def embed_query(self, text: str) -> list[float]:
            return self._hash_vector(text)

    return LocalHashEmbeddings()


# ---- simple vector store implementation ----
_store: list = []
_store_path = settings.chroma_dir / "store.json"


def _load_store():
    global _store
    if _store_path.exists():
        with open(_store_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _store = []
        for e in data:
            doc = Document(page_content=e["page_content"], metadata=e["metadata"])
            _store.append({"doc": doc, "emb": e["embedding"]})
    else:
        _store = []


def _save_store():
    settings.ensure_dirs()
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    data = []
    for entry in _store:
        data.append({
            "page_content": entry["doc"].page_content,
            "metadata": entry["doc"].metadata,
            "embedding": entry["emb"],
        })
    with open(_store_path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def _ensure_loaded():
    if not _store:
        _load_store()


def clear_store() -> None:
    # identical semantics to previous clear_chroma_dir but with a more accurate name
    print("[DEBUG] clear_store: removing existing settings.chroma_dir if present")
    if settings.chroma_dir.exists():
        shutil.rmtree(settings.chroma_dir)
    settings.ensure_dirs()
    global _store
    _store = []


class SimpleVectorStore:
    def add_documents(self, docs: List[Document]):
        _ensure_loaded()
        for doc in docs:
            emb = get_embeddings().embed_documents([doc.page_content])[0]
            _store.append({"doc": doc, "emb": emb})
        _save_store()

    def similarity_search_with_relevance_scores(
        self, query: str, k: int
    ) -> List[Tuple[Document, float]]:
        _ensure_loaded()
        q_emb = get_embeddings().embed_query(query)

        def cosine(u: list[float], v: list[float]) -> float:
            dot = sum(a * b for a, b in zip(u, v))
            nu = sum(a * a for a in u) ** 0.5
            nv = sum(b * b for b in v) ** 0.5
            if nu == 0 or nv == 0:
                return 0.0
            return dot / (nu * nv)

        scores = [(entry["doc"], cosine(q_emb, entry["emb"])) for entry in _store]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:k]


def get_vectorstore() -> SimpleVectorStore:
    settings.ensure_dirs()
    return SimpleVectorStore()