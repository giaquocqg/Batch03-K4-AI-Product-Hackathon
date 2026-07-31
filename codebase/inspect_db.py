"""
Database Inspector Script for 10 mins Study Pack.
Displays SQLite relational tables (lessons, questions) and ChromaDB vector embeddings.
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

CODEBASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODEBASE_DIR))

from database import DB_PATH, LessonDB, QuestionDB, SessionLocal


def inspect_sqlite():
    """Inspect SQLite database tables."""
    print("==================================================")
    print(f"[SQLite Database]: {DB_PATH}")
    print("==================================================")

    db = SessionLocal()
    try:
        lessons = db.query(LessonDB).all()
        print(f"\n[Lessons count]: {len(lessons)}")
        for l in lessons:
            q_count = len(l.questions) if l.questions else 0
            print(
                f"  * ID: {l.id} | Code: {l.lesson_code} | Status: {l.status} | Title: {l.title} | MCQs: {q_count}"
            )

        questions = db.query(QuestionDB).all()
        print(f"\n[MCQ Questions count]: {len(questions)}")
        for idx, q in enumerate(questions[:5], 1):
            lesson_code = q.lesson.lesson_code if q.lesson else "N/A"
            q_text = q.question_text[:70]
            print(f"  {idx}. [ID: {q.id}] [{lesson_code}] {q_text}...")
            print(
                f"     Options: {list(q.get_options().keys())} | Correct: {q.correct_option}"
            )
        if len(questions) > 5:
            print(f"     ... and {len(questions) - 5} more questions.")
    finally:
        db.close()


def inspect_chromadb():
    """Inspect ChromaDB Vector Database collections."""
    chroma_dir = CODEBASE_DIR / "chroma_db"
    print("\n==================================================")
    print(f"[ChromaDB Vector Store]: {chroma_dir}")
    print("==================================================")

    if not chroma_dir.exists():
        print("  (ChromaDB directory does not exist yet).")
        return

    try:
        import chromadb

        client = chromadb.PersistentClient(path=str(chroma_dir))
        collections = client.list_collections()
        print(f"\n[Collections count]: {len(collections)}")
        for col in collections:
            count = col.count()
            print(
                f"  * Collection: '{col.name}' | Total Chunk Vectors: {count}"
            )
            if count > 0:
                sample = col.get(limit=3)
                print("    Sample indexed chunks:")
                for doc_id, meta, doc in zip(
                    sample.get("ids", []),
                    sample.get("metadatas", []),
                    sample.get("documents", []),
                ):
                    meta_code = meta.get("lesson_code", "N/A") if meta else "N/A"
                    meta_type = meta.get("type", "N/A") if meta else "N/A"
                    snippet = doc[:80] if doc else ""
                    print(f"      - [{doc_id}] ({meta_code}/{meta_type}): {snippet}...")
    except Exception as err:
        print(f"  [Error reading ChromaDB]: {err}")


def get_db_summary_dict() -> dict:
    """Return JSON-serializable dictionary summary for Web API endpoint."""
    db = SessionLocal()
    summary = {
        "sqlite": {
            "path": str(DB_PATH),
            "lessons_count": 0,
            "questions_count": 0,
            "lessons": [],
        },
        "chromadb": {
            "path": str(CODEBASE_DIR / "chroma_db"),
            "collections": [],
        },
    }
    try:
        lessons = db.query(LessonDB).all()
        summary["sqlite"]["lessons_count"] = len(lessons)
        questions = db.query(QuestionDB).all()
        summary["sqlite"]["questions_count"] = len(questions)

        for l in lessons:
            summary["sqlite"]["lessons"].append(
                {
                    "id": l.id,
                    "lesson_code": l.lesson_code,
                    "title": l.title,
                    "status": l.status,
                    "version": l.version,
                    "questions_count": len(l.questions) if l.questions else 0,
                    "created_at": str(l.created_at),
                }
            )

        chroma_dir = CODEBASE_DIR / "chroma_db"
        if chroma_dir.exists():
            import chromadb

            client = chromadb.PersistentClient(path=str(chroma_dir))
            for col in client.list_collections():
                sample = col.get(limit=5)
                summary["chromadb"]["collections"].append(
                    {
                        "name": col.name,
                        "count": col.count(),
                        "sample_metadatas": sample.get("metadatas", []),
                        "sample_ids": sample.get("ids", []),
                    }
                )
    except Exception as err:
        summary["error"] = str(err)
    finally:
        db.close()
    return summary


if __name__ == "__main__":
    inspect_sqlite()
    inspect_chromadb()
