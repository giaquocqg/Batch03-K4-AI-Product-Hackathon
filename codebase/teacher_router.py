"""
FastAPI Router for Teacher Flow API endpoints.
Provides Upload Slide, HITL Review, Regenerate MCQ, and Approve & Publish with Vector DB Sync.
"""

import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import LessonDB, QuestionDB, get_db, init_db
from pdf_service import extract_pdf_to_markdown
from teacher_agents import regenerate_single_mcq, run_enrichment_agent, run_mcq_agent
from vector_service import sync_vector_db

router = APIRouter(prefix="/api/teacher", tags=["Teacher Flow"])

UPLOADS_DIR = Path(__file__).parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


# --- Pydantic Schemas ---

class QuestionReviewSchema(BaseModel):
    id: Optional[str] = None
    question_text: str
    options: Dict[str, str]
    correct_option: str
    explanation: Optional[str] = ""
    is_approved: bool = False


class ReviewRequestSchema(BaseModel):
    lesson_id: str
    title: Optional[str] = None
    enrich_summary: Optional[str] = None
    keywords: Optional[List[str]] = None
    questions: Optional[List[QuestionReviewSchema]] = None


class RegenerateMcqSchema(BaseModel):
    lesson_id: str
    question_id: str
    custom_instruction: Optional[str] = None


# --- Endpoints ---

@router.post("/upload-slide")
async def upload_slide(
    file: UploadFile = File(...),
    teacher_notes: str = Form(""),
    lesson_code: str = Form(...),
    title: str = Form(""),
    db: Session = Depends(get_db),
):
    """Upload slide PDF and teacher notes, run AI Agents, and return DRAFT for HITL Review."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ hỗ trợ upload file định dạng PDF (.pdf)",
        )

    # Save PDF file to uploads directory
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4().hex}_{Path(file.filename).name}"
    saved_pdf_path = UPLOADS_DIR / unique_filename

    contents = await file.read()
    with open(saved_pdf_path, "wb") as f:
        f.write(contents)

    pdf_url = f"/uploads/{unique_filename}"

    # Step 1: Extract PDF to Markdown
    try:
        pdf_markdown = extract_pdf_to_markdown(saved_pdf_path)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi đọc file PDF: {str(err)}",
        )

    # Step 2: Run Enrichment Agent
    try:
        enrich_result = run_enrichment_agent(
            pdf_markdown=pdf_markdown,
            teacher_notes=teacher_notes,
            lesson_title_or_code=title or lesson_code,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi AI Enrichment Agent: {str(err)}",
        )

    final_title = enrich_result.get("title") or title or lesson_code
    enrich_summary = enrich_result.get("enrich_summary", "")
    keywords = enrich_result.get("keywords", [])

    # Step 3: Run MCQ Generation Agent
    try:
        raw_mcqs = run_mcq_agent(
            enrich_summary=enrich_summary,
            pdf_markdown=pdf_markdown,
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi AI MCQ Agent: {str(err)}",
        )

    # Check if a lesson with this lesson_code already exists to determine version
    existing_lesson = (
        db.query(LessonDB)
        .filter(LessonDB.lesson_code == lesson_code)
        .order_by(LessonDB.version.desc())
        .first()
    )
    next_version = (existing_lesson.version + 1) if existing_lesson else 1

    # Step 4: Save DRAFT record to DB
    new_lesson = LessonDB(
        id=str(uuid.uuid4()),
        lesson_code=lesson_code,
        title=final_title,
        pdf_url=pdf_url,
        teacher_notes=teacher_notes,
        enrich_summary=enrich_summary,
        version=next_version,
        status="DRAFT",
    )
    new_lesson.set_keywords(keywords)
    db.add(new_lesson)
    db.flush()

    db_questions = []
    for mcq in raw_mcqs:
        q_item = QuestionDB(
            id=str(uuid.uuid4()),
            lesson_id=new_lesson.id,
            question_text=mcq["question_text"],
            correct_option=mcq["correct_option"],
            explanation=mcq.get("explanation", ""),
            is_approved=False,
        )
        q_item.set_options(mcq["options"])
        db.add(q_item)
        db_questions.append(q_item)

    db.commit()
    db.refresh(new_lesson)

    return {
        "status": "success",
        "message": "Đã xử lý slide & tạo DRAFT thành công. Mời Giảng viên kiểm duyệt (HITL).",
        "lesson": {
            "id": new_lesson.id,
            "lesson_code": new_lesson.lesson_code,
            "title": new_lesson.title,
            "pdf_url": new_lesson.pdf_url,
            "teacher_notes": new_lesson.teacher_notes,
            "enrich_summary": new_lesson.enrich_summary,
            "keywords": new_lesson.get_keywords(),
            "version": new_lesson.version,
            "status": new_lesson.status,
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "options": q.get_options(),
                    "correct_option": q.correct_option,
                    "explanation": q.explanation,
                    "is_approved": q.is_approved,
                }
                for q in db_questions
            ],
        },
    }


@router.put("/review")
async def review_lesson(
    payload: ReviewRequestSchema,
    db: Session = Depends(get_db),
):
    """HITL Review endpoint: Allows teacher to edit summary, keywords, and individual questions."""
    lesson = db.query(LessonDB).filter(LessonDB.id == payload.lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bài học.",
        )

    if payload.title is not None:
        lesson.title = payload.title
    if payload.enrich_summary is not None:
        lesson.enrich_summary = payload.enrich_summary
    if payload.keywords is not None:
        lesson.set_keywords(payload.keywords)

    if payload.questions is not None:
        for q_data in payload.questions:
            if q_data.id:
                q_db = (
                    db.query(QuestionDB)
                    .filter(
                        QuestionDB.id == q_data.id,
                        QuestionDB.lesson_id == lesson.id,
                    )
                    .first()
                )
                if q_db:
                    q_db.question_text = q_data.question_text
                    q_db.set_options(q_data.options)
                    q_db.correct_option = q_data.correct_option
                    q_db.explanation = q_data.explanation
                    q_db.is_approved = q_data.is_approved

    db.commit()
    db.refresh(lesson)

    return {
        "status": "success",
        "message": "Đã cập nhật chỉnh sửa của Giảng viên.",
        "lesson_id": lesson.id,
    }


@router.post("/regenerate-mcq")
async def regenerate_mcq(
    payload: RegenerateMcqSchema,
    db: Session = Depends(get_db),
):
    """Regenerate a single MCQ upon teacher request."""
    lesson = db.query(LessonDB).filter(LessonDB.id == payload.lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bài học.",
        )

    question = (
        db.query(QuestionDB)
        .filter(
            QuestionDB.id == payload.question_id,
            QuestionDB.lesson_id == lesson.id,
        )
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy câu hỏi.",
        )

    new_mcq = regenerate_single_mcq(
        enrich_summary=lesson.enrich_summary or "",
        custom_instruction=payload.custom_instruction,
    )

    question.question_text = new_mcq["question_text"]
    question.set_options(new_mcq["options"])
    question.correct_option = new_mcq["correct_option"]
    question.explanation = new_mcq["explanation"]
    question.is_approved = False

    db.commit()

    return {
        "status": "success",
        "question": {
            "id": question.id,
            "question_text": question.question_text,
            "options": question.get_options(),
            "correct_option": question.correct_option,
            "explanation": question.explanation,
            "is_approved": question.is_approved,
        },
    }


@router.post("/publish/{lesson_id}")
async def publish_lesson(
    lesson_id: str,
    db: Session = Depends(get_db),
):
    """Publish lesson: Versioning, DB save, and automatic Vector DB sync."""
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bài học.",
        )

    # Auto-approve all questions upon publish
    for q in lesson.questions:
        q.is_approved = True

    # Mark status as PUBLISHED
    lesson.status = "PUBLISHED"

    db.commit()

    # Step: Sync to Vector DB (Deletes old embeddings for lesson_code and adds new chunks)
    pdf_path = UPLOADS_DIR / Path(lesson.pdf_url).name if lesson.pdf_url else None
    pdf_markdown = ""
    if pdf_path and pdf_path.exists():
        try:
            pdf_markdown = extract_pdf_to_markdown(pdf_path)
        except Exception:
            pdf_markdown = ""

    vector_res = sync_vector_db(
        lesson_code=lesson.lesson_code,
        pdf_markdown=pdf_markdown,
        enrich_summary=lesson.enrich_summary or "",
    )

    return {
        "status": "success",
        "message": f"Bài học {lesson.lesson_code} (v{lesson.version}) đã được xuất bản chính thức!",
        "lesson": {
            "id": lesson.id,
            "lesson_code": lesson.lesson_code,
            "title": lesson.title,
            "version": lesson.version,
            "status": lesson.status,
            "approved_questions_count": len(lesson.questions),
        },
        "vector_db_sync": vector_res,
    }


@router.get("/lessons")
async def list_teacher_lessons(db: Session = Depends(get_db)):
    """Get list of all teacher lessons and their details."""
    lessons = db.query(LessonDB).order_by(LessonDB.updated_at.desc()).all()
    result = []
    for l in lessons:
        result.append({
            "id": l.id,
            "lesson_code": l.lesson_code,
            "title": l.title,
            "pdf_url": l.pdf_url,
            "version": l.version,
            "status": l.status,
            "keywords": l.get_keywords(),
            "questions_count": len(l.questions),
            "updated_at": l.updated_at.isoformat() if l.updated_at else None,
        })
    return {"lessons": result}


@router.get("/lesson/{lesson_id}")
async def get_teacher_lesson(lesson_id: str, db: Session = Depends(get_db)):
    """Get full details of a specific lesson by ID."""
    lesson = db.query(LessonDB).filter(LessonDB.id == lesson_id).first()
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy bài học.",
        )
    return {
        "lesson": {
            "id": lesson.id,
            "lesson_code": lesson.lesson_code,
            "title": lesson.title,
            "pdf_url": lesson.pdf_url,
            "teacher_notes": lesson.teacher_notes,
            "enrich_summary": lesson.enrich_summary,
            "keywords": lesson.get_keywords(),
            "version": lesson.version,
            "status": lesson.status,
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "options": q.get_options(),
                    "correct_option": q.correct_option,
                    "explanation": q.explanation,
                    "is_approved": q.is_approved,
                }
                for q in lesson.questions
            ],
        }
    }
