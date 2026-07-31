"""
Vector DB Pipeline for chunking documents and syncing embeddings in ChromaDB.
Purges old chunks by lesson_code upon publish/update (versioning) and enforces metadata filtering.
"""

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("VectorService")

CHROMA_DIR = Path(__file__).parent / "chroma_db"
CHROMA_DIR.mkdir(parents=True, exist_ok=True)


def _chunk_text(text: str, chunk_size: int = 400, overlap: int = 50) -> List[str]:
    """Simple paragraph/word chunking utility."""
    if not text:
        return []
    paragraphs = re.split(r"\n\s*\n", text)
    chunks = []
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_len = len(para)
        if current_length + para_len > chunk_size and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_length = para_len
        else:
            current_chunk.append(para)
            current_length += para_len

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return [c.strip() for c in chunks if c.strip()]


def _get_chroma_collection(client):
    """Retrieve or create ChromaDB collection for Study Pack lessons."""
    try:
        return client.get_or_create_collection(name="studypack_lessons")
    except Exception as err:
        logger.warning(f"Error initializing ChromaDB collection: {err}")
        return client.create_collection(name="studypack_lessons")


def sync_vector_db(
    lesson_code: str,
    pdf_markdown: str,
    enrich_summary: str,
    teacher_notes: Optional[str] = "",
) -> Dict[str, Any]:
    """Sync Vector DB for a specific lesson_code.

    PURGES (deletes) all previous vector embeddings matching lesson_code and indexes
    new chunks from PDF Markdown, Enrich Summary, and Teacher Notes.

    Args:
        lesson_code: Unique code of the lesson (e.g. 'DAY_01')
        pdf_markdown: Extracted raw slide markdown text
        enrich_summary: 10-minute enriched summary text
        teacher_notes: Speaker/lecture notes from teacher

    Returns:
        Dict with status and number of indexed chunks.
    """
    pdf_chunks = _chunk_text(pdf_markdown, chunk_size=400)
    summary_chunks = _chunk_text(enrich_summary, chunk_size=300)
    notes_chunks = _chunk_text(teacher_notes or "", chunk_size=300)

    try:
        import chromadb

        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = _get_chroma_collection(client)

        # Step 1: Purge old chunks matching lesson_code to prevent stale data
        try:
            collection.delete(where={"lesson_code": lesson_code})
            logger.info(f"Successfully purged old vector chunks for lesson_code: {lesson_code}")
        except Exception as del_err:
            logger.warning(f"No previous chunks found or delete skipped for {lesson_code}: {del_err}")

        # Step 2: Prepare new documents & metadata
        documents = []
        metadatas = []
        ids = []

        for idx, chunk in enumerate(pdf_chunks):
            documents.append(chunk)
            metadatas.append({"lesson_code": lesson_code, "status": "PUBLISHED", "type": "pdf_slide"})
            ids.append(f"{lesson_code}_pdf_{idx}")

        for idx, chunk in enumerate(summary_chunks):
            documents.append(chunk)
            metadatas.append({"lesson_code": lesson_code, "status": "PUBLISHED", "type": "enrich_summary"})
            ids.append(f"{lesson_code}_sum_{idx}")

        for idx, chunk in enumerate(notes_chunks):
            documents.append(chunk)
            metadatas.append({"lesson_code": lesson_code, "status": "PUBLISHED", "type": "teacher_notes"})
            ids.append(f"{lesson_code}_note_{idx}")

        if documents:
            collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
            )

        return {
            "status": "success",
            "provider": "ChromaDB",
            "lesson_code": lesson_code,
            "purged_old": True,
            "indexed_chunks": len(documents),
        }

    except Exception as err:
        logger.error(f"ChromaDB sync exception: {err}")
        return {
            "status": "error",
            "provider": "ChromaDB",
            "lesson_code": lesson_code,
            "detail": str(err),
        }


def query_vector_db(lesson_code: str, query: str, n_results: int = 4) -> List[str]:
    """Query ChromaDB for relevant text chunks filtered strictly by lesson_code.

    Args:
        lesson_code: Unique code of the lesson to filter by.
        query: User query text or question text to find relevant context.
        n_results: Maximum number of chunks to return.

    Returns:
        List of matching document chunk strings.
    """
    if not query or not query.strip():
        return []

    try:
        import chromadb

        client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        collection = _get_chroma_collection(client)

        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where={"lesson_code": lesson_code},
        )

        docs = results.get("documents", [[]])[0]
        return docs if docs else []

    except Exception as err:
        logger.warning(f"ChromaDB query failed for {lesson_code}: {err}")
        return []
