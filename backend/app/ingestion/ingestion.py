import csv
import re
from pathlib import Path
from typing import Dict, List
from backend.app.models.schemas import AssistantMode, KnowledgeDocument


def clean_text(raw_text: str) -> str:
    """Normalize whitespace and strip stray control characters."""
    cleaned = re.sub(r"\s+", " ", raw_text).strip()
    return cleaned

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split long documents into overlapping word/character chunks for RAG retrieval."""
    if len(text) <= chunk_size:
        return [text]

    chunks: List[str] = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end].strip())
        start += chunk_size - overlap
    return chunks


def load_and_validate_csv(file_path: str | Path) -> List[Dict]:
    """
    Read a CSV dataset of verified Health/Education materials, validate rows
    against KnowledgeDocument schema, and return chunked records ready for embedding.
    Expected CSV columns: doc_id, title, category, content, source_name, source_url
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    processed_chunks: List[Dict] = []

    with path.open(mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            try:
                doc = KnowledgeDocument(
                    doc_id=row["doc_id"].strip(),
                    title=clean_text(row["title"]),
                    category=AssistantMode(row["category"].strip().lower()),
                    content=clean_text(row["content"]),
                    source_name=clean_text(row["source_name"]),
                    source_url=row.get("source_url", "").strip() or None,
                )
            except Exception as exc:
                raise ValueError(f"Validation error at CSV row {row_num}: {exc}") from exc

            for idx, chunk in enumerate(chunk_text(doc.content)):
                processed_chunks.append(
                    {
                        "chunk_id": f"{doc.doc_id}_chunk_{idx}",
                        "doc_id": doc.doc_id,
                        "title": doc.title,
                        "category": doc.category.value,
                        "text": chunk,
                        "source_name": doc.source_name,
                        "source_url": doc.source_url,
                    }
                )

    return processed_chunks