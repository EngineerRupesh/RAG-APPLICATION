"""
================================================================================
 EMBEDDING SERVICE
--------------------------------------------------------------------------------
 Single responsibility: load the local sentence-transformer model that turns
 text into vectors. Runs on-device, no API key or network call needed after
 the model weights are downloaded once from HuggingFace.

 Everything else in the app that needs embeddings imports get_embeddings()
 from here instead of loading the model itself.
================================================================================
"""

from functools import lru_cache
from langchain_huggingface import HuggingFaceEmbeddings

import config


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """Return one shared embedding model instance (loaded once, reused everywhere)."""
    return HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL_NAME)
