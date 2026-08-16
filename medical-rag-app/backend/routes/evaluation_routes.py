"""
================================================================================
 EVALUATION ROUTES
--------------------------------------------------------------------------------
 Endpoints for retrieving RAGAS evaluation results and metrics.
 
 Endpoints:
   - GET /api/evaluation/ragas     — Retrieve cached evaluation results
   - POST /api/evaluate            — Trigger evaluation on Q&A pair
================================================================================
"""

import os
import json
import logging
from fastapi import APIRouter, HTTPException, status

from schemas import RagasResults, EvalRequest, EvalResponse, EvalMetrics
from services.evaluation_service import evaluate_rag

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Evaluation"])

RAGAS_RESULTS_FILE = os.path.join(
    os.path.dirname(__file__), "..", "ragas_results.json"
)


@router.get("/evaluation/ragas", response_model=RagasResults)
def get_ragas_results() -> RagasResults:
    """
    Retrieve RAGAS evaluation results if they exist.
    
    RAGAS (Retrieval-Augmented Generation Assessment) evaluates:
    - faithfulness: answer factually grounded in retrieved context?
    - answer_relevancy: does answer address the question?
    - context_precision: how much retrieved context is relevant?
    - context_recall: did retrieval find everything needed?
    """
    if not os.path.exists(RAGAS_RESULTS_FILE):
        # Return empty results if no evaluation has been run yet
        return RagasResults(
            summary={
                "faithfulness": 0.0,
                "answer_relevancy": 0.0,
                "context_precision": 0.0,
                "context_recall": 0.0,
            },
            details=[],
        )
    
    try:
        with open(RAGAS_RESULTS_FILE, "r") as f:
            data = json.load(f)
        return RagasResults(**data)
    except (json.JSONDecodeError, KeyError, ValueError) as e:
        # Return empty results if file is corrupted
        logger.error(f"Error reading RAGAS results: {e}")
        return RagasResults(
            summary={
                "faithfulness": 0.0,
                "answer_relevancy": 0.0,
                "context_precision": 0.0,
                "context_recall": 0.0,
            },
            details=[],
        )


@router.post("/evaluate", response_model=EvalResponse)
async def evaluate_output(payload: EvalRequest) -> EvalResponse:
    """
    Run RAGAS evaluation metrics on a question/answer/context triplet.

    - **faithfulness**      — Is the answer supported by the contexts?
    - **answer_relevancy**  — Is the answer relevant to the question?
    - **context_precision** — Are the contexts precise and on-topic?
    - **context_recall**    — (Only when `ground_truth` is provided.)

    Scores are appended to the `eval_log.jsonl` JSONL file for
    offline analysis and observability.
    
    Args:
        payload: EvalRequest containing question, answer, contexts, optional ground_truth
    
    Returns:
        EvalResponse with metrics and logged flag
    """
    if not payload.contexts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one context string is required for evaluation.",
        )

    try:
        metrics_dict = await evaluate_rag(
            question=payload.question,
            answer=payload.answer,
            contexts=payload.contexts,
            ground_truth=payload.ground_truth,
        )
    except Exception as exc:
        logger.exception("Evaluation endpoint error.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Evaluation error: {exc}",
        )

    return EvalResponse(
        metrics=EvalMetrics(**metrics_dict),
        logged=True,
    )
