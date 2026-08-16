"""
================================================================================
 DOCUMENT SERVICE
--------------------------------------------------------------------------------
 Single responsibility: coordinate chunking + vector storage for uploads and
 deletes, and keep the on-disk document registry (doc_id -> filename, chunk
 ids, timestamps) that the API uses to list and delete documents.
================================================================================
"""

import json
import uuid
import datetime
from typing import Any

import config
from services.chunking_service import load_and_chunk_pdf
from services.vector_store_service import vector_store


# --- registry persistence (doc_id -> metadata) -----------------------------
def _load_registry() -> dict[str, Any]:
    if config.METADATA_FILE.exists():
        with open(config.METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_registry(registry: dict[str, Any]) -> None:
    with open(config.METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


# --- public operations -------------------------------------------------
def add_document(file_path: str, filename: str) -> dict[str, Any]:
    """Chunk a PDF, embed + store it in FAISS, and register it."""
    chunks = load_and_chunk_pdf(file_path)
    if not chunks:
        raise ValueError("No extractable text found in this PDF.")

    # Tag every chunk with a doc_id + friendly source name for later
    # deletion and for nice citations shown in the UI.
    doc_id = str(uuid.uuid4())
    for chunk in chunks:
        chunk.metadata["doc_id"] = doc_id
        chunk.metadata["source_name"] = filename

    chunk_ids = vector_store.add_chunks(chunks)

    registry = _load_registry()
    registry[doc_id] = {
        "filename": filename,
        "chunk_ids": chunk_ids,
        "num_chunks": len(chunk_ids),
        "uploaded_at": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }
    _save_registry(registry)

    return {"doc_id": doc_id, **registry[doc_id]}


def delete_document(doc_id: str) -> bool:
    """Remove a document's vectors from FAISS and drop it from the registry."""
    registry = _load_registry()
    if doc_id not in registry:
        return False

    vector_store.delete_chunks(registry[doc_id]["chunk_ids"])
    del registry[doc_id]
    _save_registry(registry)
    return True


def list_documents() -> list[dict[str, Any]]:
    """Return metadata for every currently indexed document."""
    registry = _load_registry()
    return [{"doc_id": doc_id, **info} for doc_id, info in registry.items()]


def total_chunks() -> int:
    """Total number of chunks across all indexed documents (for /health)."""
    registry = _load_registry()
    return sum(info["num_chunks"] for info in registry.values())
