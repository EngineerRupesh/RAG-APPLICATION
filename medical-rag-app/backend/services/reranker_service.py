"""
================================================================================
 RERANKER SERVICE
--------------------------------------------------------------------------------
 Single responsibility: re-score FAISS candidates with a local cross-encoder
 model. A cross-encoder reads the question and each chunk TOGETHER, which is
 far more accurate at judging relevance than raw vector similarity alone -
 it trims the wide FAISS candidate set down to the precise top-k passed to
 the LLM, improving answer quality.
================================================================================
"""

from functools import lru_cache
from sentence_transformers import CrossEncoder
from langchain_core.documents import Document

import config


@lru_cache(maxsize=1)
def _get_model() -> CrossEncoder:
    """Load the cross-encoder model once and reuse it for every request."""
    return CrossEncoder(config.RERANKER_MODEL_NAME)


def rerank(question: str, candidates: list[Document], top_k: int) -> list[Document]:
    """Score each candidate against the question and return the best top_k."""
    if not candidates:
        return []

    pairs = [(question, doc.page_content) for doc in candidates]
    scores = _get_model().predict(pairs)

    ranked = sorted(zip(candidates, scores), key=lambda pair: pair[1], reverse=True)
    return [doc for doc, _score in ranked[:top_k]]
