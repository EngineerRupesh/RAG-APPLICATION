"""
================================================================================
 VECTOR STORE SERVICE (FAISS)
--------------------------------------------------------------------------------
 Single responsibility: every FAISS operation lives here - create the index,
 add chunks, delete chunks, similarity search, and save/load to disk.
 No other file in the app talks to FAISS directly.
================================================================================
"""

import uuid
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

import config
from services.embedding_service import get_embeddings


class VectorStoreService:
    """Thin wrapper around a persisted FAISS index."""

    def __init__(self) -> None:
        self._embeddings = get_embeddings()
        self._store: FAISS | None = self._load_from_disk()

    # --- load / save -----------------------------------------------------
    def _load_from_disk(self) -> "FAISS | None":
        """Load a previously saved index, if this isn't the first run."""
        index_file = config.VECTORSTORE_DIR / "index.faiss"
        if index_file.exists():
            return FAISS.load_local(
                str(config.VECTORSTORE_DIR),
                self._embeddings,
                allow_dangerous_deserialization=True,
            )
        return None

    def _save_to_disk(self) -> None:
        self._store.save_local(str(config.VECTORSTORE_DIR))

    def is_ready(self) -> bool:
        """Whether the index has at least one vector in it."""
        return self._store is not None

    # --- write operations --------------------------------------------------
    def add_chunks(self, chunks: list[Document]) -> list[str]:
        """Embed + store chunks, returning the ids assigned to each one."""
        ids = [str(uuid.uuid4()) for _ in chunks]
        if self._store is None:
            self._store = FAISS.from_documents(chunks, self._embeddings, ids=ids)
        else:
            self._store.add_documents(chunks, ids=ids)
        self._save_to_disk()
        return ids

    def delete_chunks(self, ids: list[str]) -> None:
        """Remove the given chunk ids from the index."""
        if self._store is not None and ids:
            self._store.delete(ids)
            self._save_to_disk()

    # --- read operations -----------------------------------------------
    def search(self, query: str, k: int) -> list[Document]:
        """Return the k chunks whose embeddings are closest to the query."""
        if self._store is None:
            return []
        return self._store.similarity_search(query, k=k)


# Single shared instance used across the whole app (loaded once at startup).
vector_store = VectorStoreService()
