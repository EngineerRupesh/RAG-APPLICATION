"""
================================================================================
 HEALTH ROUTE
--------------------------------------------------------------------------------
 Single responsibility: report system status. Suitable for load balancer /
 Docker / Kubernetes liveness & readiness probes, and drives the status dot
 in the UI header.
================================================================================
"""

from fastapi import APIRouter

import config
from schemas import HealthResponse
from services.vector_store_service import vector_store
from services import document_service

router = APIRouter(tags=["System"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        embedding_model=config.EMBEDDING_MODEL_NAME,
        llm_provider=config.LLM_PROVIDER,
        llm_model=config.get_active_model_name(),
        indexed_documents=len(document_service.list_documents()),
        indexed_chunks=document_service.total_chunks(),
        vectorstore_ready=vector_store.is_ready(),
    )
