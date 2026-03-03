from pathlib import Path
import fitz  # PyMuPDF
from langchain_core.documents import Document


def load_pdf(file_path: str) -> list[Document]:
    path = Path(file_path)
    docs: list[Document] = []

    with fitz.open(file_path) as pdf:
        for i, page in enumerate(pdf):
            text = (page.get_text("text") or "").strip()
            if not text:
                continue
            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": path.name, "page": i + 1},
                )
            )

    return docs