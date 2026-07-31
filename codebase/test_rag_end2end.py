"""
End-to-End Verification Test Script for Socratic RAG Chatbot.
Verifies purging old vectors, indexing published lesson content, and testing RAG response on wrong MCQ options.
"""

import sys
from pathlib import Path

# Add codebase path
CODEBASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODEBASE_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

from database import LessonDB, QuestionDB, SessionLocal, init_db
from socratic_service import explain_incorrect_answer
from vector_service import query_vector_db, sync_vector_db

init_db()


def test_rag_end2end():
    print("🚀 Starting RAG Chatbot End-to-End Verification Test...\n")
    db = SessionLocal()

    # 1. Fetch a published lesson from DB
    lesson = db.query(LessonDB).filter(LessonDB.status == "PUBLISHED").first()
    if not lesson:
        print("❌ No PUBLISHED lesson found in database!")
        return

    lesson_code = lesson.lesson_code
    print(f"📌 Testing with Published Lesson Code: {lesson_code}")
    print(f"   Title: {lesson.title}")

    # 2. Test Vector DB Sync & Purge
    sync_res = sync_vector_db(
        lesson_code=lesson_code,
        pdf_markdown="Slide PDF content: LLM architecture utilizes Decoder-only Transformer for autoregressive next-token prediction.",
        enrich_summary=lesson.enrich_summary or "Tóm tắt bài học: Generative AI và Agentic AI.",
        teacher_notes=lesson.teacher_notes or "Ghi chú giảng viên: Chú ý công thức Goal -> Plan -> Action.",
    )
    print(f"✅ Vector DB Sync Result: {sync_res}")

    # 3. Test Vector Search
    vector_chunks = query_vector_db(lesson_code=lesson_code, query="Agentic AI công thức", n_results=4)
    print(f"🔍 Vector Search Chunks Retrieved: {len(vector_chunks)}")
    for idx, c in enumerate(vector_chunks, 1):
        print(f"   Chunk {idx}: {c[:80]}...")

    # 4. Fetch a question from the lesson
    question = lesson.questions[0] if lesson.questions else None
    q_id = question.id if question else "q_test_001"
    q_text = question.question_text if question else "Công thức cốt lõi của Agentic AI là gì?"
    options = question.get_options() if question else {"A": "Prompt -> Content", "B": "Goal -> Plan -> Action"}
    correct_opt = question.correct_option if question else "B"
    explanation = question.explanation if question else "Agentic AI có khả năng lập kế hoạch và thực thi hành động tự động."

    user_selected = "A" if correct_opt != "A" else "B"

    print("\n--------------------------------------------------")
    print(f"📝 Testing Socratic Explanation for Wrong Answer:")
    print(f"   Câu hỏi: {q_text}")
    print(f"   Lựa chọn của học sinh (SAI): {user_selected} - {options.get(user_selected, '')}")
    print(f"   Đáp án ĐÚNG: {correct_opt} - {options.get(correct_opt, '')}")
    print("--------------------------------------------------\n")

    # 5. Call Socratic Tutor RAG Service
    res = explain_incorrect_answer(
        lesson_code=lesson_code,
        question_text=q_text,
        options=options,
        correct_option=correct_opt,
        explanation=explanation,
        user_selected_option=user_selected,
        user_message="Tại sao phương án em chọn chưa chính xác?",
        session_id="test_verify_session_001",
        db=db,
    )

    reply = res.get("reply", "")
    sources_count = res.get("rag_sources_count", 0)

    print(f"🤖 Trợ giảng Socratic Reply:\n{reply}\n")
    print(f"📊 RAG Context Sources Count: {sources_count}")

    # Assertions
    assert "Không tìm thấy tài liệu" not in reply, "❌ FAIL: Response contains rigid 'Không tìm thấy tài liệu' error!"
    assert len(reply) > 20, "❌ FAIL: Response is too short!"
    print("🎉 END-TO-END RAG VERIFICATION PASSED SUCCESSFULLY!")

    db.close()


if __name__ == "__main__":
    test_rag_end2end()
