"""
================================================================================
 EVALUATION SERVICE
--------------------------------------------------------------------------------
 Computes RAGAS metrics (Retrieval-Augmented Generation Assessment) for
 individual Q&A pairs in real-time.
 
 Metrics:
   - faithfulness: Is answer grounded in retrieved context?
   - answer_relevancy: Does answer address the question?
   - context_precision: Is retrieved context relevant?
   - context_recall: Did retrieval find everything needed?
 
 Results are logged to a JSONL file for offline analysis.
================================================================================
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)

from config import OLLAMA_BASE_URL, OLLAMA_MODEL_NAME, EMBEDDING_MODEL_NAME

try:
    from langchain_ollama import ChatOllama
    from langchain_huggingface import HuggingFaceEmbeddings
    EVALUATION_AVAILABLE = True
except ImportError:
    EVALUATION_AVAILABLE = False
    print("⚠️  RAGAS evaluation libraries not installed. Install with:")
    print("   pip install langchain-ollama langchain-huggingface datasets ragas")


class RagasEvaluator:
    """Singleton evaluator that computes RAGAS metrics for Q&A pairs."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RagasEvaluator, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized or not EVALUATION_AVAILABLE:
            return
        
        try:
            self.llm = ChatOllama(
                base_url=OLLAMA_BASE_URL,
                model=OLLAMA_MODEL_NAME,
                temperature=0.0
            )
            self.embeddings = HuggingFaceEmbeddings(
                model_name=EMBEDDING_MODEL_NAME
            )
            self._initialized = True
        except Exception as e:
            print(f"Failed to initialize RAGAS evaluator: {e}")
            self._initialized = False


async def evaluate_qa(question: str, answer: str, contexts: list[str]) -> dict:
    """
    Evaluate a single Q&A pair using RAGAS metrics.
    
    Args:
        question: The user's question
        answer: The generated answer
        contexts: List of context snippets from retrieved sources
    
    Returns:
        Dictionary with faithfulness, answer_relevancy, context_precision, context_recall scores
    """
    if not EVALUATION_AVAILABLE:
        return {
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "context_precision": 0.0,
            "context_recall": 0.0,
            "error": "RAGAS evaluation libraries not installed"
        }
    
    try:
        evaluator = RagasEvaluator()
        if not evaluator._initialized:
            return {
                "faithfulness": 0.0,
                "answer_relevancy": 0.0,
                "context_precision": 0.0,
                "context_recall": 0.0,
                "error": "RAGAS evaluator not initialized"
            }
        
        # Prepare data in RAGAS format
        eval_data = {
            "question": [question],
            "answer": [answer],
            "contexts": [contexts or [""]],  # Empty list would fail
            "ground_truth": [""],  # Not used for answer-only evaluation
        }
        
        # Create dataset and evaluate (run in executor to avoid blocking)
        loop = asyncio.get_event_loop()
        dataset = Dataset.from_dict(eval_data)
        
        results = await loop.run_in_executor(
            None,
            lambda: evaluate(
                dataset=dataset,
                metrics=[
                    faithfulness,
                    answer_relevancy,
                    context_precision,
                    context_recall,
                ],
                llm=evaluator.llm,
                embeddings=evaluator.embeddings
            )
        )
        
        # Extract scores from results
        scores = {
            "faithfulness": float(results["faithfulness"][0]),
            "answer_relevancy": float(results["answer_relevancy"][0]),
            "context_precision": float(results["context_precision"][0]),
            "context_recall": float(results["context_recall"][0]),
        }
        
        return scores
        
    except Exception as e:
        print(f"Error evaluating Q&A: {e}")
        return {
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
            "context_precision": 0.0,
            "context_recall": 0.0,
            "error": str(e)
        }


def _log_evaluation(question: str, answer: str, contexts: list, metrics: dict, ground_truth: str = None):
    """
    Log evaluation results to JSONL file for observability and offline analysis.
    
    Args:
        question: User's question
        answer: Generated answer
        contexts: Retrieved context snippets
        metrics: RAGAS metrics dict
        ground_truth: Optional ground truth answer
    """
    try:
        eval_log_path = Path(__file__).parent.parent / "eval_log.jsonl"
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "question": question,
            "answer": answer,
            "contexts_count": len(contexts),
            "ground_truth": ground_truth,
            "metrics": {
                "faithfulness": metrics.get("faithfulness", 0.0),
                "answer_relevancy": metrics.get("answer_relevancy", 0.0),
                "context_precision": metrics.get("context_precision", 0.0),
                "context_recall": metrics.get("context_recall", 0.0),
            }
        }
        
        with open(eval_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Failed to log evaluation: {e}")


async def evaluate_rag(
    question: str, 
    answer: str, 
    contexts: list[str],
    ground_truth: str = None
) -> dict:
    """
    Evaluate RAG output using RAGAS metrics and log results.
    
    This is the main entry point for evaluation. It can be called with or without
    ground truth. Metrics are computed and logged to eval_log.jsonl.
    
    Args:
        question: The user's question
        answer: The generated answer
        contexts: List of context snippets from retrieved sources
        ground_truth: Optional ground truth answer for context_recall evaluation
    
    Returns:
        Dictionary with faithfulness, answer_relevancy, context_precision, context_recall scores
    """
    # Get evaluation metrics
    metrics = await evaluate_qa(question, answer, contexts)
    
    # Log to JSONL file
    _log_evaluation(question, answer, contexts, metrics, ground_truth)
    
    return metrics
