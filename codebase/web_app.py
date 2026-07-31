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
from fastapi import Depends, FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

# Add codebase path
CODEBASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = CODEBASE_DIR.parent

sys.path.insert(0, str(CODEBASE_DIR))

from database import get_db, init_db
from teacher_router import router as teacher_router
from student_routes import router as student_router
from study_pack_generator import (
    MissingAPIKeyError,
    UnsupportedObjectiveError,
    generate_study_pack,
    _load_env_file,
)
from transcript_parser import parse_transcript
from inspect_db import get_db_summary_dict

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


@app.get("/api/admin/db-inspect")
async def inspect_database():
    """Inspect SQLite tables and ChromaDB vector collections."""
    return get_db_summary_dict()


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
    lesson_code: Optional[str] = None
    transcript: Optional[str] = None
    question: str
    search_query: Optional[str] = None
    question_id: Optional[str] = None


@app.post("/api/chat")
async def chat_endpoint(payload: ChatRequest, request: Request, db: Session = Depends(get_db)):
    """RAG Chatbot endpoint for answering free-form questions about the published teacher lesson."""
    client_host = request.client.host if request.client else "127.0.0.1"
    lesson_code = payload.lesson_code or payload.transcript or "DAY_01"

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

    # 3. MCQ-aware: If question_id provided, look up structured MCQ data from DB
    from database import LessonDB, QuestionDB
    from vector_service import query_vector_db
    from reranker import rerank_chunks
    from study_pack_generator import _get_api_provider, _load_env_file
    import logging
    chat_logger = logging.getLogger("ChatEndpoint")

    mcq_question_text = ""
    mcq_options = {}
    mcq_correct_option = ""
    mcq_explanation = ""
    mcq_user_choice = ""

    if payload.question_id:
        q_item = db.query(QuestionDB).filter(QuestionDB.id == payload.question_id).first()
        if q_item:
            mcq_question_text = q_item.question_text
            mcq_options = q_item.get_options()
            mcq_correct_option = q_item.correct_option
            mcq_explanation = q_item.explanation or ""

    # Determine search query: use question_text from DB if available, else search_query, else user question
    search_q = mcq_question_text or payload.search_query or sanitized_question
    raw_chunks = query_vector_db(lesson_code=lesson_code, query=search_q, n_results=8)
    rag_chunks = rerank_chunks(query=search_q, chunks=raw_chunks, top_k=3)

    # Also retrieve lesson context from relational DB
    lesson = (
        db.query(LessonDB)
        .filter(
            (LessonDB.lesson_code == lesson_code) | (LessonDB.id == lesson_code),
        )
        .first()
    )
    db_summary = ""
    if lesson and lesson.enrich_summary:
        db_summary = lesson.enrich_summary[:500]

    # Build context for LLM
    rag_context = "\n---\n".join(rag_chunks) if rag_chunks else ""
    combined_context = f"{rag_context}\n{db_summary}".strip()
    if not combined_context:
        combined_context = f"Bài học {lesson_code}."

    # 4. Build prompt — MCQ-aware if question_id was resolved
    system_prompt = (
        "Bạn là trợ lý giảng dạy AI (phong cách Socratic) cho học viên khóa AI Thực Chiến.\n"
        "Trả lời câu hỏi dựa trên ngữ cảnh bài giảng được cung cấp.\n"
        "Quy tắc: Chỉ dùng thông tin trong ngữ cảnh. Không bịa đặt. "
        "Trả lời đầy đủ, chi tiết, dễ hiểu bằng tiếng Việt (ít nhất 80 từ).\n"
        "PHÂN BIỆT KHÁI NIỆM: Tính ổn định/ít ngẫu nhiên -> Temperature. "
        "Chi phí token tiếng Việt -> Subword/Tokenization. KHÔNG nhầm lẫn."
    )

    if mcq_explanation:
        # MCQ mode: build a structured prompt with question context
        correct_text = mcq_options.get(mcq_correct_option, mcq_correct_option)
        opts_text = ", ".join(f"{k}. {v}" for k, v in mcq_options.items()) if mcq_options else ""
        user_prompt = (
            f"Học sinh hỏi: {sanitized_question}\n\n"
            f"THÔNG TIN CÂU HỎI TRẮC NGHIỆM:\n"
            f"- Câu hỏi: {mcq_question_text}\n"
            f"- Phương án: {opts_text}\n"
            f"- Đáp án đúng: {mcq_correct_option}. {correct_text}\n"
            f"- Giải thích chuẩn: {mcq_explanation}\n\n"
            f"<RETRIEVED_CONTEXT>\n{combined_context}\n</RETRIEVED_CONTEXT>\n\n"
            f"Hãy giải thích tại sao đáp án đúng là {mcq_correct_option}, "
            f"và phân tích ngắn gọn vì sao các phương án khác chưa chính xác. "
            f"Dựa vào bài giảng để minh họa."
        )
    else:
        # Free-form Q&A mode
        user_prompt = (
            f"Câu hỏi: {sanitized_question}\n\n"
            f"<RETRIEVED_CONTEXT>\n{combined_context}\n</RETRIEVED_CONTEXT>"
        )

    answer = ""
    _load_env_file()
    try:
        provider, api_key = _get_api_provider()
        if provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            import os
            model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
            model = genai.GenerativeModel(model_name, system_instruction=system_prompt)
            response = model.generate_content(
                user_prompt,
                generation_config={"temperature": 0.3, "max_output_tokens": 600},
            )
            answer = response.text or ""
        elif provider == "openai":
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=600,
            )
            answer = response.choices[0].message.content or ""
    except Exception as llm_err:
        chat_logger.warning(f"LLM call failed: {llm_err}")

    # 5. Quality check + Structured fallback
    # If LLM response is too short (<50 chars) or empty, use structured fallback
    _answer_too_short = len(answer.strip()) < 50
    if not answer or _answer_too_short:
        if mcq_explanation:
            # Best case: use DB explanation for MCQ
            correct_text = mcq_options.get(mcq_correct_option, mcq_correct_option)
            answer = (
                f"**Câu hỏi:** {mcq_question_text}\n\n"
                f"**Đáp án đúng: {mcq_correct_option}. {correct_text}**\n\n"
                f"> {mcq_explanation}\n\n"
            )
            # Add brief analysis of wrong options
            for opt_key, opt_val in mcq_options.items():
                if opt_key != mcq_correct_option:
                    answer += f"- **{opt_key}. {opt_val}** — Không đúng vì đây không phải đặc điểm phân biệt cốt lõi theo bài giảng.\n"
            answer += (
                f"\n*(Hệ thống đang dùng chế độ giải thích từ ngân hàng câu hỏi. "
                f"Thử lại sau ít phút để nhận phân tích chi tiết hơn từ AI.)*"
            )
        elif rag_chunks:
            best_chunk = rag_chunks[0][:400]
            answer = (
                f"Theo nội dung bài giảng:\n\n> {best_chunk}\n\n"
                f"*(Hệ thống đang tạm dùng chế độ trích dẫn trực tiếp do API đang quá tải. "
                f"Vui lòng thử lại sau ít phút để nhận câu trả lời chi tiết hơn.)*"
            )
        else:
            answer = (
                "Xin lỗi, hiện tại hệ thống đang tạm thời quá tải. "
                "Vui lòng thử lại sau ít phút."
            )

    return {"status": "success", "answer": answer}


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
