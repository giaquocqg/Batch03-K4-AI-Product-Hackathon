"""
Unit and Integration tests for Student Flow API endpoints,
Socratic Tutor Agent, and Feynman Reverse Role Agent.
"""

import json
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, LessonDB, QuestionDB, get_db
from web_app import app

client = TestClient(app)


def setup_published_lesson():
    """Helper to seed DB with a published lesson and MCQs for testing."""
    db_file = "codebase/studypack.db"
    engine = create_engine(f"sqlite:///{db_file}")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    # Check if lesson already exists
    existing = session.query(LessonDB).filter(LessonDB.lesson_code == "DAY_STUDENT_TEST").first()
    if not existing:
        lesson = LessonDB(
            id="test-student-lesson-001",
            lesson_code="DAY_STUDENT_TEST",
            title="Kiến trúc AI Agent & RAG Pipeline",
            pdf_url="/uploads/test_student.pdf",
            teacher_notes="Ghi chú giảng viên về RAG và Socratic Tutor",
            enrich_summary="Bài giảng tóm tắt 10 phút về RAG Pipeline, Vector Database ChromaDB và AI Agents.",
            version=1,
            status="PUBLISHED",
        )
        lesson.set_keywords(["RAG", "ChromaDB", "Vector Search", "Socratic Agent", "Feynman Mode"])
        session.add(lesson)
        session.flush()

        question = QuestionDB(
            id="q-student-001",
            lesson_id=lesson.id,
            question_text="Vai trò chính của Vector Database trong kiến trúc RAG là gì?",
            correct_option="A",
            explanation="Vector DB lưu trữ các chunk văn bản dưới dạng vector embeddings để truy xuất ngữ cảnh chính xác.",
            is_approved=True,
        )
        question.set_options({
            "A": "Lưu trữ và tìm kiếm vector embeddings của tài liệu",
            "B": "Huấn luyện lại mô hình LLM từ đầu",
            "C": "Chuyển đổi giao diện người dùng",
            "D": "Tạo dữ liệu giả lập cho hệ thống",
        })
        session.add(question)
        session.commit()
    session.close()


def test_get_published_lessons():
    """Test GET /api/student/lessons returns list of published lessons."""
    setup_published_lesson()

    response = client.get("/api/student/lessons")
    assert response.status_code == 200
    data = response.json()
    assert "lessons" in data
    assert isinstance(data["lessons"], list)
    assert len(data["lessons"]) > 0

    codes = [l["lesson_code"] for l in data["lessons"]]
    assert "DAY_STUDENT_TEST" in codes


def test_get_published_lesson_detail():
    """Test GET /api/student/lessons/{lesson_code} returns full study pack data."""
    setup_published_lesson()

    response = client.get("/api/student/lessons/DAY_STUDENT_TEST")
    assert response.status_code == 200
    data = response.json()

    assert data["lesson_code"] == "DAY_STUDENT_TEST"
    assert data["title"] == "Kiến trúc AI Agent & RAG Pipeline"
    assert len(data["keywords"]) > 0
    assert len(data["questions"]) == 1
    assert data["questions"][0]["id"] == "q-student-001"
    assert data["questions"][0]["correct_option"] == "A"


def test_socratic_explain_endpoint():
    """Test POST /api/student/chat/explain for Chatbot 1 (Socratic Tutor)."""
    setup_published_lesson()

    payload = {
        "lesson_code": "DAY_STUDENT_TEST",
        "question_id": "q-student-001",
        "user_selected_option": "B",
        "user_message": "Em nghĩ B đúng vì Vector DB giúp huấn luyện LLM?",
        "session_id": "test_socratic_session_001",
    }

    response = client.post("/api/student/chat/explain", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert "session_id" in data
    assert "reply" in data
    assert isinstance(data["reply"], str)
    assert len(data["reply"]) > 0


def test_feynman_start_endpoint():
    """Test POST /api/student/chat/feynman/start for Chatbot 2."""
    setup_published_lesson()

    payload = {
        "lesson_code": "DAY_STUDENT_TEST",
    }

    response = client.post("/api/student/chat/feynman/start", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert "session_id" in data
    assert "initial_message" in data
    assert isinstance(data["initial_message"], str)
    assert len(data["initial_message"]) > 0


def test_feynman_respond_endpoint():
    """Test POST /api/student/chat/feynman/respond for Chatbot 2."""
    setup_published_lesson()

    start_payload = {"lesson_code": "DAY_STUDENT_TEST"}
    start_res = client.post("/api/student/chat/feynman/start", json=start_payload).json()
    session_id = start_res["session_id"]

    respond_payload = {
        "session_id": session_id,
        "lesson_code": "DAY_STUDENT_TEST",
        "student_answer": "Vector Database dùng để lưu trữ các đoạn văn bản chuyển đổi thành vector (embeddings) giúp tìm kiếm ngữ cảnh nhanh chóng.",
    }

    response = client.post("/api/student/chat/feynman/respond", json=respond_payload)
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "success"
    assert data["session_id"] == session_id
    assert "reply" in data
    assert isinstance(data["reply"], str)
    assert len(data["reply"]) > 0
