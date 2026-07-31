"""
Socratic Tutor Agent Service (Chatbot 1).
Provides polite, concept-focused explanations for wrong MCQ answers and guides students' thinking.
Uses ChromaDB Vector Search (RAG) + Relational DB Fallback and retains session chat memory.
"""

import logging
import os
import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from database import LessonDB, QuestionDB, SessionLocal
from study_pack_generator import _get_api_provider, _load_env_file
from vector_service import query_vector_db
from reranker import rerank_chunks

logger = logging.getLogger("SocraticService")

# Global session memory store: session_id -> list of message dicts {"role": str, "content": str}
SOCRATIC_SESSION_MEMORY: Dict[str, List[Dict[str, str]]] = {}


def get_or_create_session(session_id: Optional[str] = None) -> str:
    """Return existing session_id or generate a new UUID session key."""
    if not session_id or session_id not in SOCRATIC_SESSION_MEMORY:
        sid = session_id or f"socratic_{uuid.uuid4().hex[:12]}"
        SOCRATIC_SESSION_MEMORY[sid] = []
        return sid
    return session_id


def get_session_history(session_id: str) -> List[Dict[str, str]]:
    """Retrieve message history for a session."""
    return SOCRATIC_SESSION_MEMORY.get(session_id, [])


def add_message_to_history(session_id: str, role: str, content: str) -> None:
    """Append a user or assistant message to session memory."""
    if session_id not in SOCRATIC_SESSION_MEMORY:
        SOCRATIC_SESSION_MEMORY[session_id] = []
    SOCRATIC_SESSION_MEMORY[session_id].append({"role": role, "content": content})


SOCRATIC_SYSTEM_PROMPT = """Bạn là Trợ giảng Socratic tận tụy, lịch sự và thân thiện của ứng dụng "10 mins Study Pack".

NHIỆM VỤ:
Giải thích cho sinh viên khi họ trả lời chưa đúng câu hỏi trắc nghiệm hoặc cần hướng dẫn thêm về kiến thức bài học.

NGUYÊN TẮC HƯỚNG DẪN:
1. Độ dài ngắn gọn BẮT BUỘC dưới 150 từ (tiếng Việt).
2. Tuyệt đối KHÔNG chỉ trích. Giải thích lý do tại sao phương án sinh viên chọn chưa chính xác dựa trên bản chất khái niệm.
3. Sử dụng ngữ cảnh tài liệu bài học được cung cấp để hướng dẫn sinh viên.
4. Tuyệt đối KHÔNG báo lỗi "Không tìm thấy tài liệu phù hợp" khi bài học đã xuất bản. Nếu vector search ngắn, hãy dùng chính phần giải thích của giảng viên và nội dung tóm tắt để giải thích.
5. PHÂN BIỆT KHÁI NIỆM TRỌNG TÂM: Khi câu hỏi liên quan tới độ ngẫu nhiên, tính ổn định -> BẮT BUỘC giải thích dựa trên tham số Temperature / Top_p. KHÔNG nhầm lẫn sang chi phí Subword / Tokenization.
6. Giữ giọng văn ân cần, động viên và cởi mở.
"""


def _call_socratic_llm(
    system_prompt: str,
    history: List[Dict[str, str]],
    user_prompt: str,
) -> str:
    """Execute multi-turn LLM call for Socratic Tutor using OpenAI or Gemini."""
    _load_env_file()
    try:
        provider, api_key = _get_api_provider()
    except Exception as err:
        logger.warning(f"No API key available, using fallback: {err}")
        return (
            "Chào bạn! Khái niệm này liên quan trực tiếp đến nội dung cốt lõi của bài học. "
            "Khi xét câu hỏi này, bạn hãy chú ý đến điều kiện tiên quyết và mục tiêu của từng lựa chọn. "
            "Theo bạn, điểm khác biệt chính giữa lựa chọn của bạn và đáp án chuẩn là gì?"
        )

    if provider == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_prompt})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4,
            max_tokens=350,
        )
        return response.choices[0].message.content or ""

    elif provider == "gemini":
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        gemini_model_name = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

        history_text = ""
        for msg in history:
            role_label = "Học sinh" if msg["role"] == "user" else "Trợ giảng Socratic"
            history_text += f"{role_label}: {msg['content']}\n"

        full_prompt = (
            f"{system_prompt}\n\n"
            f"--- LỊCH SỬ TRÒ CHUYỆN ---\n{history_text}\n"
            f"--- YÊU CẦU MỚI ---\n{user_prompt}"
        )

        try:
            model = genai.GenerativeModel(gemini_model_name)
            res = model.generate_content(
                full_prompt,
                generation_config={"temperature": 0.4, "max_output_tokens": 350},
            )
            return res.text or ""
        except Exception as llm_err:
            logger.warning(f"Gemini API call failed ({llm_err}). Using Socratic fallback response.")
            return (
                "Chào bạn! Dựa trên nội dung bài giảng, khi xét câu hỏi này bạn hãy chú ý đến "
                "bản chất khái niệm cốt lõi và các điều kiện tiên quyết được giảng viên nhấn mạnh. "
                "Phương án bạn chọn chưa phản ánh chính xác mục tiêu của bài học. "
                "Theo bạn, điểm khác biệt chính giữa lựa chọn của bạn và đáp án chuẩn là gì?"
            )

    raise RuntimeError(f"Unsupported provider: {provider}")


def explain_incorrect_answer(
    lesson_code: str,
    question_text: str,
    options: Dict[str, str],
    correct_option: str,
    explanation: Optional[str] = "",
    user_selected_option: Optional[str] = None,
    user_message: Optional[str] = "",
    session_id: Optional[str] = None,
    db: Optional[Session] = None,
) -> Dict[str, Any]:
    """Socratic Agent entrypoint to explain wrong MCQ answer or question doubt.

    4-Step Hybrid Pipeline:
    1. Extract payload: lesson_code, question_text, user_answer, correct_answer, explanation.
    2. Vector Retrieval: Query ChromaDB for lesson_code (PUBLISHED).
    3. Relational DB Fallback: Always retrieve lesson enrich_summary, teacher_notes, and q.explanation.
    4. Prompting: Socratic tutor explanation <150 words. NEVER return 'Không tìm thấy tài liệu'.
    """
    sid = get_or_create_session(session_id)
    history = get_session_history(sid)

    if not isinstance(options, dict):
        options = {}

    user_opt_val = options.get(user_selected_option, "") if user_selected_option else ""
    correct_opt_val = options.get(correct_option, "") if correct_option else ""

    user_answer_text = f"{user_selected_option}. {user_opt_val}" if user_selected_option else "N/A"
    correct_answer_text = f"{correct_option}. {correct_opt_val}" if correct_option else "N/A"

    # FIX: Search query uses ONLY question_text + correct answer context (no user_message pollution)
    search_query = f"{question_text} {correct_opt_val} {explanation or ''}".strip()
    raw_rag_chunks = query_vector_db(lesson_code=lesson_code, query=search_query, n_results=8)
    rag_chunks = rerank_chunks(query=search_query, chunks=raw_rag_chunks, top_k=3)

    # 2. Database Fallback Retrieval (Relational DB)
    close_db_after_use = False
    active_db = db
    if active_db is None:
        active_db = SessionLocal()
        close_db_after_use = True

    db_context_parts = []
    try:
        lesson = (
            active_db.query(LessonDB)
            .filter(
                (LessonDB.lesson_code == lesson_code) | (LessonDB.id == lesson_code),
            )
            .first()
        )
        if lesson:
            if lesson.enrich_summary:
                db_context_parts.append(f"Bài giảng tóm tắt: {lesson.enrich_summary[:500]}")
            if lesson.teacher_notes:
                db_context_parts.append(f"Ghi chú giảng viên: {lesson.teacher_notes[:400]}")
    except Exception as err:
        logger.warning(f"Database context query exception: {err}")
    finally:
        if close_db_after_use:
            active_db.close()

    # Combine RAG vector chunks + Relational DB context
    rag_text = "\n---\n".join(rag_chunks) if rag_chunks else ""
    db_text = "\n---\n".join(db_context_parts) if db_context_parts else ""

    combined_context = f"{rag_text}\n{db_text}".strip()
    if not combined_context:
        combined_context = f"Nội dung bài học {lesson_code}. Giải thích chính thức: {explanation or 'Giải thích dựa trên bản chất môn học.'}"

    # 3. Construct System & User Prompt according to exact specification
    user_prompt = f"""Bạn là trợ giảng. Học sinh vừa làm sai câu hỏi sau:
- Câu hỏi: {question_text}
- Đáp án học sinh chọn: {user_answer_text} (SAI)
- Đáp án đúng: {correct_answer_text}
- Giải thích có sẵn: {explanation or 'Chưa có'}

Dựa vào nội dung bài giảng dưới đây:
---
{combined_context}
---
{user_message or 'Hãy giải thích ngắn gọn (dưới 150 từ), thân thiện lý do tại sao đáp án của học sinh chưa đúng và hướng dẫn học sinh hiểu lại cho đúng dựa trên bài giảng.'}"""

    # 4. Call LLM
    reply_text = _call_socratic_llm(
        system_prompt=SOCRATIC_SYSTEM_PROMPT,
        history=history,
        user_prompt=user_prompt,
    )

    # FIX: Structured fallback when LLM API fails (quota/timeout/no-key)
    # Priority: explanation from DB > rag_chunks context > generic message
    _is_generic_fallback = (
        not reply_text
        or "chú ý đến bản chất khái niệm" in reply_text
        or "chú ý đến điều kiện tiên quyết" in reply_text
    )
    if _is_generic_fallback:
        if explanation:
            # Best case: DB has the correct explanation for this question
            reply_text = (
                f"Chào bạn! Câu hỏi này liên quan đến: **{question_text}**\n\n"
                f"Đáp án đúng là **{correct_answer_text}**.\n\n"
                f"> {explanation}\n\n"
            )
            if user_selected_option and user_selected_option != correct_option:
                reply_text += (
                    f"Lựa chọn của bạn ({user_answer_text}) chưa chính xác. "
                    f"Hãy đối chiếu lại bản chất khái niệm trong bài giảng để ghi nhớ nhé!"
                )
        else:
            # No explanation from DB — use question context + rag summary
            rag_hint = rag_chunks[0][:200] if rag_chunks else ""
            reply_text = (
                f"Chào bạn! Đáp án đúng cho câu hỏi này là **{correct_answer_text}**.\n\n"
            )
            if rag_hint:
                reply_text += f"Theo nội dung bài giảng:\n> {rag_hint}...\n\n"
            reply_text += (
                f"Bạn hãy xem lại phần bài giảng liên quan đến câu hỏi "
                f"*\"{question_text[:60]}...\"* để nắm vững kiến thức nhé!"
            )

    # Save to session memory
    user_log_msg = user_message or f"Giải thích lý do em chọn {user_selected_option} chưa đúng"
    add_message_to_history(sid, "user", user_log_msg)
    add_message_to_history(sid, "assistant", reply_text)

    return {
        "status": "success",
        "session_id": sid,
        "reply": reply_text,
        "rag_sources_count": len(rag_chunks),
        "sources": rag_chunks,
    }
