"""
================================================================================
 SCHEMAS MODULE
--------------------------------------------------------------------------------
 Pydantic models describing the shape of every request/response body used by
 the API. FastAPI uses these for automatic validation + OpenAPI docs.
================================================================================
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Body sent by the frontend text field when the user asks a question."""
    question: str = Field(..., min_length=1, description="User's medical question (text only)")


class SourceChunk(BaseModel):
    """A single retrieved chunk that backed the generated answer."""
    document: str
    page: Optional[int] = None
    snippet: str


class RagasScoresSingle(BaseModel):
    """RAGAS evaluation scores for a single answer."""
    faithfulness: float = 0.0
    answer_relevancy: float = 0.0
    context_precision: float = 0.0
    context_recall: float = 0.0
    error: Optional[str] = None


class ChatResponse(BaseModel):
    """Response returned after running the RAG chain."""
    answer: str
    sources: List[SourceChunk] = []
    ragas: Optional[RagasScoresSingle] = None


class DocumentInfo(BaseModel):
    """Metadata describing one uploaded & indexed PDF."""
    doc_id: str
    filename: str
    num_chunks: int
    uploaded_at: str


class DeleteResponse(BaseModel):
    """Confirmation payload returned after a document is deleted."""
    doc_id: str
    deleted: bool
    message: str


class HealthResponse(BaseModel):
    """Payload returned by GET /health."""
    status: str
    embedding_model: str
    llm_provider: str
    llm_model: str
    indexed_documents: int
    indexed_chunks: int
    vectorstore_ready: bool


class RagasScores(BaseModel):
    """Individual RAGAS metric scores."""
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float


class RagasDetail(BaseModel):
    """RAGAS scores for a single evaluation question."""
    question: str
    faithfulness: float
    answer_relevancy: float
    context_precision: float
    context_recall: float


class RagasResults(BaseModel):
    """Complete RAGAS evaluation results."""
    summary: RagasScores
    details: List[RagasDetail] = []


class EvalMetrics(BaseModel):
    """RAGAS evaluation metrics for a single answer."""
    faithfulness: float = 0.0
    answer_relevancy: float = 0.0
    context_precision: float = 0.0
    context_recall: float = 0.0
    error: Optional[str] = None


class EvalRequest(BaseModel):
    """Request body for POST /api/evaluate endpoint."""
    question: str = Field(..., min_length=1, description="User's question")
    answer: str = Field(..., min_length=1, description="Generated answer to evaluate")
    contexts: List[str] = Field(..., min_items=1, description="Retrieved context snippets")
    ground_truth: Optional[str] = Field(None, description="Optional ground truth answer for recall evaluation")


class EvalResponse(BaseModel):
    """Response from POST /api/evaluate endpoint."""
    metrics: EvalMetrics
    logged: bool = True
