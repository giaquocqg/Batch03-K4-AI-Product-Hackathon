"""
Database models and connection setup for 10 mins Study Pack using SQLAlchemy & SQLite.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_PATH = Path(__file__).parent / "studypack.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class LessonDB(Base):
    """Database model for lessons."""

    __tablename__ = "lessons"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lesson_code = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    pdf_url = Column(String, nullable=True)
    teacher_notes = Column(Text, nullable=True)
    enrich_summary = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)  # Stored as JSON string
    version = Column(Integer, default=1, nullable=False)
    status = Column(String, default="DRAFT", nullable=False)  # DRAFT, PUBLISHED
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    questions = relationship(
        "QuestionDB", back_populates="lesson", cascade="all, delete-orphan"
    )

    def get_keywords(self) -> List[str]:
        if not self.keywords:
            return []
        try:
            return json.loads(self.keywords)
        except Exception:
            return []

    def set_keywords(self, kw_list: List[str]) -> None:
        self.keywords = json.dumps(kw_list, ensure_ascii=False)


class QuestionDB(Base):
    """Database model for multiple choice questions."""

    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lesson_id = Column(String, ForeignKey("lessons.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    options = Column(Text, nullable=False)  # Stored as JSON string {"A": "", ...}
    correct_option = Column(String(5), nullable=False)
    explanation = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False, nullable=False)

    lesson = relationship("LessonDB", back_populates="questions")

    def get_options(self) -> Dict[str, str]:
        if not self.options:
            return {}
        try:
            return json.loads(self.options)
        except Exception:
            return {}

    def set_options(self, opts: Dict[str, str]) -> None:
        self.options = json.dumps(opts, ensure_ascii=False)


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for obtaining DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
