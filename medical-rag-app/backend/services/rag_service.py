"""
================================================================================
 RAG SERVICE (LCEL chain)
--------------------------------------------------------------------------------
 Single responsibility: wire the other services together into the actual
 retrieval-augmented-generation chain:

     question -> FAISS search (vector_store_service)
              -> rerank      (reranker_service)
              -> format context
              -> prompt -> LLM (llm_service)
              -> answer

 This file only orchestrates - it never talks to FAISS, the reranker model,
 or the LLM provider directly, it calls the dedicated service for each.
================================================================================
"""

from operator import itemgetter
from typing import Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.documents import Document

import config
from services.vector_store_service import vector_store
from services.reranker_service import rerank
from services.llm_service import get_llm

# ---------------------------------------------------------------------------
# System prompt - keeps the LLM grounded ONLY in retrieved context and adds
# a safety disclaimer appropriate for a medical-information assistant.
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """You are a careful medical-information assistant.
Answer the user's question using ONLY the context below, which was extracted
from documents the user uploaded (e.g. clinical guidelines, patient
leaflets, research notes).

Rules you must always follow:
1. Base your answer strictly on the provided context - never invent facts
   that are not supported by it.
2. If the context does not contain enough information to answer, say so
   plainly instead of guessing.
3. Never provide a personal diagnosis or prescribe treatment. Present the
   information factually and remind the user to consult a licensed
   healthcare professional for decisions about their own care.
4. Be clear and concise, and where useful, mention which source document
   the information came from.

Context:
{context}
"""


def _retrieve_and_rerank(question: str) -> list[Document]:
    """Step 1+2: FAISS search for a wide candidate set, then rerank it down."""
    candidates = vector_store.search(question, k=config.RETRIEVE_K)
    return rerank(question, candidates, top_k=config.RERANK_TOP_K)


def _format_context(docs: list[Document]) -> str:
    """Step 3: turn the final reranked chunks into one context string."""
    parts = []
    for d in docs:
        source = d.metadata.get("source_name", "unknown document")
        page = d.metadata.get("page", "?")
        parts.append(f"[{source} - page {page}]\n{d.page_content}")
    return "\n\n---\n\n".join(parts)


def _build_chain():
    """Assemble the LCEL chain from the pieces above."""
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("human", "{question}")]
    )

    retrieve_step = itemgetter("question") | RunnableLambda(_retrieve_and_rerank)

    generate_answer = (
        {
            "context": itemgetter("source_documents") | RunnableLambda(_format_context),
            "question": itemgetter("question"),
        }
        | prompt
        | get_llm()
        | StrOutputParser()
    )

    # Retrieve once, reuse the reranked docs both for the answer's grounding
    # context and for the "sources" returned to the caller.
    return RunnableParallel(
        question=itemgetter("question"),
        source_documents=retrieve_step,
    ) | RunnableParallel(
        answer=generate_answer,
        source_documents=itemgetter("source_documents"),
    )


def answer_question(question: str) -> dict[str, Any]:
    """Run the full RAG chain end-to-end. Returns {"answer": str, "sources": [...]}."""
    if not vector_store.is_ready():
        return {
            "answer": (
                "No documents have been uploaded yet. Please upload a medical "
                "PDF so I have something to search before answering questions."
            ),
            "sources": [],
        }

    chain = _build_chain()
    result = chain.invoke({"question": question})

    sources = [
        {
            "document": d.metadata.get("source_name", "unknown"),
            "page": d.metadata.get("page"),
            "snippet": d.page_content[:300],
        }
        for d in result["source_documents"]
    ]
    return {"answer": result["answer"], "sources": sources}
