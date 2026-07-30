"""
Unit tests for Teacher Flow API, DB Models, PDF Extraction, and Vector DB Sync.
"""

import json
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, LessonDB, QuestionDB, get_db
from pdf_service import extract_pdf_to_markdown
from vector_service import sync_vector_db
from web_app import app

client = TestClient(app)


def test_pdf_extraction_fallback(tmp_path):
    """Test extracting PDF content or returning fallback markdown for invalid path."""
    fake_pdf = tmp_path / "test.pdf"
    fake_pdf.write_bytes(b"%PDF-1.4 Fake PDF Content")
    
    res = extract_pdf_to_markdown(fake_pdf)
    assert isinstance(res, str)
    assert len(res) > 0


def test_database_models(tmp_path):
    """Test creating and querying LessonDB and QuestionDB objects."""
    db_file = tmp_path / "test_studypack.db"
    engine = create_engine(f"sqlite:///{db_file}")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    lesson = LessonDB(
        id="lesson-001",
        lesson_code="DAY_99",
        title="Test Lesson",
        pdf_url="/uploads/test.pdf",
        teacher_notes="Test notes",
        enrich_summary="Test summary",
        version=1,
        status="DRAFT",
    )
    lesson.set_keywords(["AI", "LLM", "Test"])
    session.add(lesson)
    session.flush()

    question = QuestionDB(
        id="q-001",
        lesson_id=lesson.id,
        question_text="Test Question 1?",
        correct_option="A",
        explanation="Explanation text",
        is_approved=False,
    )
    question.set_options({"A": "Opt A", "B": "Opt B", "C": "Opt C", "D": "Opt D"})
    session.add(question)
    session.commit()

    saved_lesson = session.query(LessonDB).filter(LessonDB.id == "lesson-001").first()
    assert saved_lesson is not None
    assert saved_lesson.lesson_code == "DAY_99"
    assert saved_lesson.get_keywords() == ["AI", "LLM", "Test"]
    assert len(saved_lesson.questions) == 1
    assert saved_lesson.questions[0].get_options()["A"] == "Opt A"

    session.close()


def test_vector_db_sync():
    """Test Vector DB synchronization logic."""
    res = sync_vector_db(
        lesson_code="TEST_SYNC_01",
        pdf_markdown="## Slide 1\n\nAI Foundation and Agentic AI Architecture.",
        enrich_summary="Bài giảng 10 phút về AI Agentic và RAG Pipeline.",
    )
    assert res["status"] in ("success", "success_fallback")
    assert res["lesson_code"] == "TEST_SYNC_01"
    assert res["indexed_chunks"] > 0


def test_teacher_lessons_list_api():
    """Test GET /api/teacher/lessons endpoint."""
    response = client.get("/api/teacher/lessons")
    assert response.status_code == 200
    data = response.json()
    assert "lessons" in data
    assert isinstance(data["lessons"], list)
