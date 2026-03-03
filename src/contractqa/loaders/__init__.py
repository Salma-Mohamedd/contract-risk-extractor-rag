from pathlib import Path
from langchain_core.documents import Document
from .pdf_loader import load_pdf
from .docx_loader import load_docx


def load_any(file_path: str) -> list[Document]:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return load_pdf(file_path)
    if ext == ".docx":
        return load_docx(file_path)
    raise ValueError(f"Unsupported file type: {ext}. Use PDF or DOCX.")