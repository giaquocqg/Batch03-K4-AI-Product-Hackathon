"""
Socratic Tutor Agent Service (Chatbot 1).
Provides polite, concept-focused explanations for wrong MCQ answers and guides students' thinking.
Uses ChromaDB Vector Search (RAG) and retains conversation history per session_id.
"""

import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from study_pack_generator import _get_api_provider, _load_env_file
from vector_service import query_vector_db

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


SOCRATIC_SYSTEM_PROMPT = """Bạn là Trợ giảng Socratic (Socratic Tutor Agent) tận tụy, lịch sự và thân thiện của ứng dụng "10 mins Study Pack".

NHIỆM VỤ:
Giải thích cho sinh viên khi họ trả lời chưa đúng câu hỏi trắc nghiệm hoặc cần hướng dẫn thêm về kiến thức bài học.

NGUYÊN TẮC SOCRATIC & PHONG CÁCH:
1. Độ dài ngắn gọn BẮT BUỘC dưới 150 từ (tiếng Việt).
2. Không chỉ trích hay chỉ vội bảo "sai rồi". Hãy giải thích lý do tại sao lựa chọn hiện tại chưa chính xác dựa trên bản chất khái niệm.
3. Liên hệ với kiến thức cốt lõi trong tài liệu bài học được cung cấp.
4. Kết thúc lời đáp bằng một câu hỏi gợi mở tư duy (Socratic Prompting) để sinh viên tự suy ngẫm và điều chỉnh câu trả lời.
5. Giữ giọng văn ân cần, động viên và cởi mở.
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
        logger.warning(f"No API key available, using intelligent fallback response: {err}")
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
            max_tokens=300,
        )
        return response.choices[0].message.content or ""

    elif provider == "gemini":
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        gemini_model_name = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")

        # Format context for Gemini prompt
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
        except Exception:
            model = genai.GenerativeModel("gemini-3.5-flash")
            res = model.generate_content(
                full_prompt,
                generation_config={"temperature": 0.4, "max_output_tokens": 350},
            )
            return res.text or ""

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
) -> Dict[str, Any]:
    """Socratic Agent entrypoint to explain wrong MCQ answer or question doubt.

    Args:
        lesson_code: Lesson identifier for RAG retrieval.
        question_text: Content of MCQ question.
        options: Dict of MCQ options {"A": "...", ...}
        correct_option: Correct option letter ("A", "B", etc.)
        explanation: Teacher's official explanation.
        user_selected_option: Student's selected option letter.
        user_message: Additional query/comment from student.
        session_id: Optional chat session ID for multi-turn history.

    Returns:
        Dict with session_id, reply text, and vector sources context.
    """
    sid = get_or_create_session(session_id)
    history = get_session_history(sid)

    # Step 1: Query Vector DB (RAG) for matching lesson chunks
    search_query = f"{question_text} {explanation or ''}"
    rag_chunks = query_vector_db(lesson_code=lesson_code, query=search_query, n_results=2)
    rag_context = "\n---\n".join(rag_chunks) if rag_chunks else "Không có thêm trích dẫn từ slide."

    # Format options string
    options_str = "\n".join([f"{k}. {v}" for k, v in options.items()])
    user_choice_str = (
        f"Lựa chọn của học sinh: {user_selected_option} - {options.get(user_selected_option, '')}"
        if user_selected_option
        else "Học sinh chưa chọn đáp án cụ thể."
    )

    user_prompt = f"""--- CÂU HỎI TRẮC NGHIỆM ---
Nội dung câu hỏi: {question_text}
Các phương án:
{options_str}

{user_choice_str}
Đáp án đúng chính thức: {correct_option} - {options.get(correct_option, '')}
Giải thích của giảng viên: {explanation or 'Chưa có giải thích chi tiết.'}

--- TÀI LIỆU BÀI HỌC (VECTOR DB RAG CONTEXT) ---
{rag_context}

--- THẮC MẮC BỔ SUNG CỦA HỌC SINH ---
{user_message or 'Hỏi AI giải thích thêm lý do tại sao phương án tôi chọn chưa đúng.'}

Hãy đóng vai Trợ giảng Socratic giải thích cho học sinh hiểu bản chất khái niệm và gợi mở tư duy."""

    reply_text = _call_socratic_llm(
        system_prompt=SOCRATIC_SYSTEM_PROMPT,
        history=history,
        user_prompt=user_prompt,
    )

    # Save to session memory
    user_log_msg = user_message or f"Giải thích giúp em câu hỏi này (em chọn {user_selected_option})"
    add_message_to_history(sid, "user", user_log_msg)
    add_message_to_history(sid, "assistant", reply_text)

    return {
        "status": "success",
        "session_id": sid,
        "reply": reply_text,
        "rag_sources_count": len(rag_chunks),
        "sources": rag_chunks,
    }
