"""
================================================================================
 CONFIG MODULE
--------------------------------------------------------------------------------
 Centralized application settings, loaded from environment variables (.env).
 Keeping everything in one place makes the app easy to configure for
 different environments (local dev, staging, production) without touching
 any business logic code.
================================================================================
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load variables from a .env file if present (does nothing in prod if absent)
load_dotenv(override=True)

# ---------------------------------------------------------------------------
# Base paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"                 # raw uploaded PDFs live here
VECTORSTORE_DIR = BASE_DIR / "vectorstore"         # FAISS index files live here
METADATA_FILE = VECTORSTORE_DIR / "metadata.json"  # doc_id -> chunk mapping

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Embedding model (runs 100% locally, no API key / internet call needed
# after the first download of the model weights from HuggingFace)
# ---------------------------------------------------------------------------
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

# ---------------------------------------------------------------------------
# LLM provider settings
# Supported values for LLM_PROVIDER: "openai" | "anthropic" | "gemini" | "ollama"
# ---------------------------------------------------------------------------
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL_NAME = os.getenv("ANTHROPIC_MODEL_NAME", "claude-sonnet-4-6")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")

# Local Llama via Ollama - runs 100% on your machine, no API key, no internet
# call at inference time. Requires Ollama installed + running (ollama.com)
# and the model pulled once: `ollama pull llama3.1`
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3.1")

LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.0"))


def get_active_model_name() -> str:
    """Return the model name for whichever LLM_PROVIDER is currently active."""
    return {
        "gemini": GEMINI_MODEL_NAME,
        "anthropic": ANTHROPIC_MODEL_NAME,
        "openai": OPENAI_MODEL_NAME,
        "ollama": OLLAMA_MODEL_NAME,
    }.get(LLM_PROVIDER, OPENAI_MODEL_NAME)

# ---------------------------------------------------------------------------
# RAG pipeline tuning knobs
# ---------------------------------------------------------------------------
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))

# FAISS returns this many candidates first (wide net)...
RETRIEVE_K = int(os.getenv("RETRIEVE_K", "10"))
# ...then the reranker narrows it down to this many for the LLM (precise set)
RERANK_TOP_K = int(os.getenv("RERANK_TOP_K", "4"))

# Local cross-encoder model used to rerank retrieved chunks
RERANKER_MODEL_NAME = os.getenv("RERANKER_MODEL_NAME", "cross-encoder/ms-marco-MiniLM-L-6-v2")

# ---------------------------------------------------------------------------
# Server settings
# ---------------------------------------------------------------------------
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
