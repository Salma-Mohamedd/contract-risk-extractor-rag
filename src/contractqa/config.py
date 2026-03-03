from dataclasses import dataclass
from pathlib import Path

# automatically load variables from a .env file if present
from dotenv import load_dotenv

load_dotenv()  # no-op if .env does not exist


@dataclass(frozen=True)
class Settings:
    project_root: Path = Path(__file__).resolve().parents[2]
    data_dir: Path = project_root / "data"
    uploads_dir: Path = data_dir / "uploads"
    chroma_dir: Path = data_dir / "chroma"

    collection_name: str = "contracts_single_doc"

    chunk_size: int = 1000
    chunk_overlap: int = 150

    top_k: int = 6
    min_relevance: float = 0.35  # 0..1 (higher = better)

    # OpenAI models (no local LLM install needed)
    openai_chat_model: str = "gpt-4o-mini"
    openai_embed_model: str = "text-embedding-3-small"

    temperature: float = 0.0

    def ensure_dirs(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()