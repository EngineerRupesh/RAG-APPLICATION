"""
================================================================================
 CHAT ROUTE
--------------------------------------------------------------------------------
 Single responsibility: HTTP layer for asking a question. This is the only
 way the user talks to the assistant - a plain text field, no voice input
 anywhere in this app. The actual RAG chain lives in services/rag_service.py.
 
 Also computes RAGAS metrics in real-time to evaluate answer quality.
================================================================================
"""

from fastapi import APIRouter

from schemas import ChatRequest, ChatResponse, RagasScoresSingle
from services.rag_service import answer_question
from services.evaluation_service import evaluate_rag

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # 1. Get RAG answer
    result = answer_question(request.question)
    answer = result["answer"]
    sources = result["sources"]
    
    # 2. Extract context snippets for evaluation
    contexts = [s["snippet"] for s in sources] if sources else []
    
    # 3. Evaluate answer quality (async, non-blocking)
    ragas_scores = await evaluate_rag(
        question=request.question,
        answer=answer,
        contexts=contexts,
        ground_truth=None
    )
    
    ragas = RagasScoresSingle(**ragas_scores)
    
    return ChatResponse(answer=answer, sources=sources, ragas=ragas)
