"""
FastAPI Router for Student Flow API Endpoints.
Provides Published Lessons lookup, Quick Quiz Study Pack delivery,
Socratic Tutor Chatbot (wrong answer explanation), and Feynman Mode Chatbot.
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import LessonDB, QuestionDB, get_db
from feynman_service import respond_feynman_session, start_feynman_session
from socratic_service import explain_incorrect_answer

router = APIRouter(prefix="/api/student", tags=["Student Flow"])


# --- Request & Response Schemas ---

class SocraticExplainRequest(BaseModel):
    lesson_code: str = Field(..., description="Unique code of the lesson (e.g. DAY_01)")
    question_id: Optional[str] = Field(None, description="Optional ID of the MCQ question")
    user_selected_option: Optional[str] = Field(None, description="Option selected by student ('A', 'B', 'C', 'D')")
    user_message: Optional[str] = Field("", description="Optional student question/comment")
    session_id: Optional[str] = Field(None, description="Optional session ID for chat memory")


class FeynmanStartRequest(BaseModel):
    lesson_code: str = Field(..., description="Unique code of the lesson")


class FeynmanRespondRequest(BaseModel):
    session_id: str = Field(..., description="Active Feynman chat session ID")
    lesson_code: str = Field(..., description="Unique code of the lesson")
    student_answer: str = Field(..., description="Explanation from student acting as teacher")


# --- Endpoints ---

@router.get("/lessons")
async def list_published_lessons(db: Session = Depends(get_db)):
    """GET /api/student/lessons

    Returns list of all published lessons for students.
    """
    lessons = (
        db.query(LessonDB)
        .filter(LessonDB.status == "PUBLISHED")
        .order_by(LessonDB.updated_at.desc())
        .all()
    )

    result = []
    for l in lessons:
        result.append({
            "id": l.id,
            "lesson_code": l.lesson_code,
            "title": l.title,
            "pdf_url": l.pdf_url,
            "version": l.version,
            "keywords": l.get_keywords(),
            "questions_count": len(l.questions),
            "updated_at": l.updated_at.isoformat() if l.updated_at else None,
        })

    return {"lessons": result}


import re

def extract_key_points(summary_text: str) -> List[str]:
    if not summary_text:
        return []
    lines = [line.strip() for line in summary_text.splitlines() if line.strip()]
    bullets = [re.sub(r'^\s*[\-\*\d\.]+\s*', '', line) for line in lines if re.match(r'^\s*[\-\*\d\.]+\s+', line)]
    if len(bullets) >= 3:
        return bullets[:5]
    paragraphs = [p.strip() for p in summary_text.split('\n\n') if p.strip() and not p.startswith('#')]
    if len(paragraphs) >= 3:
        return paragraphs[:5]
    sentences = [s.strip() for s in re.split(r'[\.\!\?]\s+', summary_text) if s.strip()]
    return sentences[:5]


@router.get("/lessons/{lesson_code}")
async def get_published_lesson(lesson_code: str, db: Session = Depends(get_db)):
    """GET /api/student/lessons/{lesson_code}

    Returns full Study Pack JSON for a published lesson:
    title, pdf_url, enrich_summary, key_points, keywords, version, questions.
    Supports lookup by lesson_code or primary key id.
    """
    lesson = (
        db.query(LessonDB)
        .filter(
            (LessonDB.lesson_code == lesson_code) | (LessonDB.id == lesson_code),
            LessonDB.status == "PUBLISHED",
        )
        .first()
    )

    if not lesson:
        # Fallback search if not published yet, for development preview
        lesson = (
            db.query(LessonDB)
            .filter((LessonDB.lesson_code == lesson_code) | (LessonDB.id == lesson_code))
            .first()
        )
        if not lesson:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy bài học published cho mã: {lesson_code}",
            )

    return {
        "id": lesson.id,
        "lesson_code": lesson.lesson_code,
        "title": lesson.title,
        "pdf_url": lesson.pdf_url,
        "enrich_summary": lesson.enrich_summary,
        "key_points": extract_key_points(lesson.enrich_summary),
        "keywords": lesson.get_keywords(),
        "teacher_notes": lesson.teacher_notes,
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


@router.post("/chat/explain")
async def chat_socratic_explain(
    payload: SocraticExplainRequest,
    db: Session = Depends(get_db),
):
    """POST /api/student/chat/explain

    Chatbot 1: Socratic Tutor Agent for explaining wrong answers and guiding conceptual thinking.
    """
    question_text = "Thắc mắc chung về bài học"
    options = {}
    correct_option = "N/A"
    explanation = ""

    if payload.question_id:
        q_item = (
            db.query(QuestionDB)
            .filter(QuestionDB.id == payload.question_id)
            .first()
        )
        if q_item:
            question_text = q_item.question_text
            options = q_item.get_options()
            correct_option = q_item.correct_option
            explanation = q_item.explanation or ""

    # FIX: When question_id is missing, try fuzzy lookup by matching user_message
    # against question_text in the DB for this lesson
    if correct_option == "N/A" and payload.user_message:
        _msg = payload.user_message[:120].strip()
        if len(_msg) > 15:
            lesson_obj = (
                db.query(LessonDB)
                .filter(
                    (LessonDB.lesson_code == payload.lesson_code)
                    | (LessonDB.id == payload.lesson_code),
                )
                .first()
            )
            if lesson_obj:
                for q_candidate in lesson_obj.questions:
                    if q_candidate.question_text[:50] in _msg or _msg[:50] in q_candidate.question_text:
                        question_text = q_candidate.question_text
                        options = q_candidate.get_options()
                        correct_option = q_candidate.correct_option
                        explanation = q_candidate.explanation or ""
                        break

    res = explain_incorrect_answer(
        lesson_code=payload.lesson_code,
        question_text=question_text,
        options=options,
        correct_option=correct_option,
        explanation=explanation,
        user_selected_option=payload.user_selected_option,
        user_message=payload.user_message,
        session_id=payload.session_id,
        db=db,
    )

    return res


@router.post("/chat/feynman/start")
async def chat_feynman_start(
    payload: FeynmanStartRequest,
    db: Session = Depends(get_db),
):
    """POST /api/student/chat/feynman/start

    Chatbot 2: Feynman Mode Reverse Role Agent. Initiates session with curious student persona.
    """
    import logging
    _logger = logging.getLogger("FeynmanRoute")
    try:
        lesson = (
            db.query(LessonDB)
            .filter(LessonDB.lesson_code == payload.lesson_code)
            .order_by(LessonDB.version.desc())
            .first()
        )

        enrich_summary = lesson.enrich_summary if lesson else "Nội dung tổng quan bài học 10 phút."
        title = lesson.title if lesson else payload.lesson_code

        res = start_feynman_session(
            lesson_code=payload.lesson_code,
            enrich_summary=enrich_summary or "",
            title=title,
        )
        return res
    except Exception as e:
        _logger.error(f"Feynman start error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Không thể khởi tạo phiên Feynman: {str(e)}",
        )


@router.post("/chat/feynman/respond")
async def chat_feynman_respond(
    payload: FeynmanRespondRequest,
    db: Session = Depends(get_db),
):
    """POST /api/student/chat/feynman/respond

    Chatbot 2: Feynman Mode Reverse Role Agent. Evaluates student explanation and responds.
    """
    import logging
    _logger = logging.getLogger("FeynmanRoute")
    try:
        lesson = (
            db.query(LessonDB)
            .filter(LessonDB.lesson_code == payload.lesson_code)
            .order_by(LessonDB.version.desc())
            .first()
        )

        enrich_summary = lesson.enrich_summary if lesson else ""

        res = respond_feynman_session(
            session_id=payload.session_id,
            lesson_code=payload.lesson_code,
            student_answer=payload.student_answer,
            enrich_summary=enrich_summary,
        )
        return res
    except Exception as e:
        _logger.error(f"Feynman respond error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Không thể phản hồi: {str(e)}",
        )
