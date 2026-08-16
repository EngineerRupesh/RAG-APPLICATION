"""
================================================================================
 DOCUMENT ROUTES
--------------------------------------------------------------------------------
 Single responsibility: HTTP layer for managing the knowledge base - upload
 a PDF, list what's indexed, delete a document. All real work is delegated
 to services/document_service.py.
================================================================================
"""

import shutil
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException

import config
from schemas import DocumentInfo, DeleteResponse
from services import document_service

router = APIRouter(prefix="/api/documents", tags=["Documents"])


@router.post("", response_model=DocumentInfo)
async def upload_document(file: UploadFile = File(...)) -> DocumentInfo:
    """Upload a PDF - it is chunked, embedded, and added to the FAISS index."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    dest_path = config.UPLOAD_DIR / f"{uuid.uuid4()}.pdf"
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        info = document_service.add_document(str(dest_path), filename=file.filename)
    except Exception as exc:
        dest_path.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"Failed to process PDF: {exc}")

    return DocumentInfo(
        doc_id=info["doc_id"],
        filename=info["filename"],
        num_chunks=info["num_chunks"],
        uploaded_at=info["uploaded_at"],
    )


@router.get("", response_model=list[DocumentInfo])
def list_documents() -> list[DocumentInfo]:
    """List every document currently indexed in the knowledge base."""
    return [
        DocumentInfo(
            doc_id=d["doc_id"],
            filename=d["filename"],
            num_chunks=d["num_chunks"],
            uploaded_at=d["uploaded_at"],
        )
        for d in document_service.list_documents()
    ]


@router.delete("/{doc_id}", response_model=DeleteResponse)
def delete_document(doc_id: str) -> DeleteResponse:
    """Delete a document: removes its vectors from FAISS and its registry entry."""
    if not document_service.delete_document(doc_id):
        raise HTTPException(status_code=404, detail="Document not found.")
    return DeleteResponse(doc_id=doc_id, deleted=True, message="Document removed from the index.")
