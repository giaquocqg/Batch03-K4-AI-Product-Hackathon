"""
10 mins Study Pack — Full-Stack FastAPI Backend.
Integrates Teacher Flow (Slide Upload, HITL Review, MCQ Gen, Publish & Vector Sync)
and Student Flow (Study Pack generation & Citation viewer).
"""

import json
import os
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Add codebase path
CODEBASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CODEBASE_DIR.parent

sys.path.insert(0, str(CODEBASE_DIR))

from database import init_db
from teacher_router import router as teacher_router
from student_routes import router as student_router
from study_pack_generator import (
    MissingAPIKeyError,
    UnsupportedObjectiveError,
    generate_study_pack,
    _load_env_file,
)
from transcript_parser import parse_transcript

# Initialize DB tables
init_db()

# Load environment variables from .env
_load_env_file()

app = FastAPI(
    title="10 mins Study Pack API",
    description="AI-Powered Study Pack Platform with Teacher HITL Flow and Student Study Flow",
    version="2.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(teacher_router)
app.include_router(student_router)

# Directories
UPLOADS_DIR = CODEBASE_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
WEB_DIR = CODEBASE_DIR / "web"
TRANSCRIPT_DIR = REPO_ROOT / "data" / "vlearn-pack" / "transcript"

app.mount("/uploads", StaticFiles(directory=str(UPLOADS_DIR)), name="uploads")


# --- Student Flow Legacy API Endpoints ---

@app.get("/api/transcripts")
async def list_transcripts():
    """List available transcript files for Student Flow."""
    files = sorted(TRANSCRIPT_DIR.glob("transcript-??-clean.md"))
    return {"transcripts": [f.name for f in files]}


@app.post("/api/generate")
async def generate_student_study_pack(request: Request):
    """Generate 10-minute Study Pack from transcript for Student Flow."""
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must be valid JSON.",
        )

    transcript_name = payload.get("transcript")
    objective = payload.get("objective", "Ôn quiz trong 10 phút")

    if not transcript_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Hãy chọn một transcript trong danh sách.",
        )

    transcript_path = TRANSCRIPT_DIR / transcript_name
    if not transcript_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Không tìm thấy transcript: {transcript_name}",
        )

    try:
        parsed = parse_transcript(transcript_path)
        study_pack, metadata = generate_study_pack(
            transcript=parsed,
            objective=objective,
        )
        return {
            "status": "success",
            "study_pack": study_pack,
            "metadata": metadata,
        }
    except UnsupportedObjectiveError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err),
        )
    except MissingAPIKeyError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(err),
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi tạo Study Pack: {str(err)}",
        )


from typing import Optional

class ChatRequest(BaseModel):
    transcript: str
    question: str
    search_query: Optional[str] = None


@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest, request: Request):
    """RAG Chatbot endpoint for answering questions about the lesson."""
    client_host = request.client.host if request.client else "127.0.0.1"
    transcript_name = payload.transcript

    try:
        import re
        match = re.search(r"transcript-(\d+)-clean", transcript_name)
        if match:
            transcript_id = f"T{match.group(1)}"
        else:
            transcript_id = transcript_name
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Định dạng transcript không đúng.",
        )

    # 1. Rate Limiting Check
    from guardrails import check_rate_limit, RateLimitExceeded, sanitize_chat_query
    try:
        check_rate_limit(client_host)
    except RateLimitExceeded as e:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e),
        )

    # 2. Guardrails Check
    try:
        sanitized_question = sanitize_chat_query(payload.question)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # 3. Query RAG
    from rag_engine import query_rag
    try:
        s_query = payload.search_query.strip() if (payload.search_query and payload.search_query.strip()) else None
        res = query_rag(sanitized_question, transcript_id, search_query=s_query)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi RAG Query: {str(e)}",
        )


@app.get("/api/citation")
async def get_citation(transcript: str, code: str):
    """Get specific citation text segment for Student Flow."""
    transcript_path = TRANSCRIPT_DIR / transcript
    if not transcript_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File transcript không tồn tại.",
        )

    parsed = parse_transcript(transcript_path)
    for seg in parsed.segments:
        if seg.code == code:
            return {
                "status": "success",
                "code": seg.code,
                "text": seg.text,
                "has_unclear": seg.has_unclear,
                "is_activity": seg.is_activity,
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Không tìm thấy citation {code}",
    )


# --- Serve Frontend Static Files ---

@app.get("/{file_path:path}")
async def serve_frontend(file_path: str):
    """Serve frontend static files (index.html, styles.css, app.js, etc.)."""
    if not file_path or file_path == "/":
        file_path = "index.html"
    
    target_path = WEB_DIR / file_path
    if target_path.exists() and target_path.is_file():
        return FileResponse(target_path)
    
    # Default fallback to index.html
    index_path = WEB_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    
    raise HTTPException(status_code=404, detail="File not found.")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    print("🚀 10 mins Study Pack FastAPI server starting at http://127.0.0.1:8000")
    uvicorn.run("web_app:app", host="127.0.0.1", port=8000, reload=True)
