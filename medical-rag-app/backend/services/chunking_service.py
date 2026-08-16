"""
================================================================================
 CHUNKING SERVICE
--------------------------------------------------------------------------------
 Single responsibility: load a PDF from disk and split it into overlapping,
 retrieval-sized text chunks. No embedding, no storage - just text in,
 chunked LangChain Documents out.
================================================================================
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

import config


def load_and_chunk_pdf(file_path: str) -> list[Document]:
    """Load every page of a PDF and split it into overlapping text chunks."""
    pages = PyPDFLoader(file_path).load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_documents(pages)
