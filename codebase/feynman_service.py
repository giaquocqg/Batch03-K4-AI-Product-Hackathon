"""
Feynman Mode - Reverse Role Chatbot Agent Service (Chatbot 2).
LLM acts as a curious/naive student seeking learning, while the Student user acts as the Teacher/Expert.
Applies Socratic prompting to encourage deep understanding via teaching (Feynman Technique).
"""

import logging
import os
import uuid
from typing import Any, Dict, List, Optional

from study_pack_generator import _get_api_provider

logger = logging.getLogger("FeynmanService")

# Global Feynman session memory store: session_id -> list of messages {"role": str, "content": str}
FEYNMAN_SESSION_MEMORY: Dict[str, List[Dict[str, str]]] = {}
FEYNMAN_SESSION_LESSON: Dict[str, Dict[str, Any]] = {}

# Model đã được kiểm chứng hoạt động, tốc độ nhanh tương đương chatbot trợ lý
_FEYNMAN_MODEL_PRIMARY = "gemini-3.5-flash-lite"
_FEYNMAN_MODEL_FALLBACK = "gemini-2.5-flash"

# Fix #3: Giới hạn độ dài enrich_summary để không làm phình prompt
_SUMMARY_MAX_CHARS = 800

FEYNMAN_SYSTEM_PROMPT = """<role>Bạn là một học sinh tò mò, lễ phép đang nhờ người dùng (đóng vai Thầy giáo/Chuyên gia) giải thích bài học này.</role>

<rules>
- Nếu Thầy giáo giải thích đúng và dễ hiểu: Hãy khen chân thành và đặt một câu hỏi đào sâu hơn hoặc một tình huống thực tế liên quan đến bài học.
- Nếu Thầy giáo giải thích chưa chính xác hoặc mơ hồ: KHÔNG ĐƯỢC chỉ trích hay bảo "Thầy sai rồi". Hãy đóng vai học sinh thắc mắc: "Dạ thưa Thầy, em chưa hiểu rõ chỗ [X], nếu như [tình huống bẫy] thì sao ạ?" để gợi mở cho người dùng tự điều chỉnh tư duy.
- Giữ giọng văn tự nhiên, lễ phép, cầu thị và ngắn gọn (dưới 150 từ).
</rules>
"""

FEYNMAN_INITIAL_PROMPT = """Bạn là một học sinh tò mò, lễ phép đang muốn bắt đầu học bài học dưới đây từ người dùng (đóng vai Thầy giáo).

--- NỘI DUNG BÀI GIẢNG TÓM TẮT ---
{enrich_summary}

NHIỆM VỤ:
Dựa vào bài giảng tóm tắt ở trên, hãy đưa ra một lời chào lễ phép và đặt BỘ CÂU HỎI MỞ ĐẦU TÒ MÒ (1-2 câu hỏi ngắn) nhờ Thầy giáo giải thích bản chất khái niệm chính của bài học này.
Đảm bảo giữ lời chào và câu hỏi tự nhiên, lịch sự, dưới 100 từ.
"""


def _call_feynman_llm(
    system_prompt: str,
    history: List[Dict[str, str]],
    user_prompt: str,
) -> str:
    """Execute multi-turn LLM call for Feynman Mode using OpenAI or Gemini."""
    # Fix #2: Không gọi _load_env_file() ở đây nữa — đã được gọi tại startup (web_app.py)
    # _get_api_provider() nội bộ có gọi _load_env_file() nên vẫn đảm bảo env được load
    try:
        provider, api_key = _get_api_provider()
    except Exception as err:
        logger.warning(f"No API key available, using fallback for Feynman mode: {err}")
        return (
            "Dạ thưa Thầy, em thấy bài học này rất hay! "
            "Thầy có thể giải thích giúp em khái niệm quan trọng nhất trong bài này được áp dụng như thế nào không ạ?"
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
            temperature=0.5,
            max_tokens=800,
        )
        return response.choices[0].message.content or ""

    elif provider == "gemini":
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        # Fix #1: Ưu tiên env var, fallback về model đúng tên
        gemini_model_name = os.environ.get("GEMINI_MODEL", _FEYNMAN_MODEL_PRIMARY)

        history_text = ""
        for msg in history:
            role_label = "Thầy giáo (Người dùng)" if msg["role"] == "user" else "Học sinh (AI)"
            history_text += f"{role_label}: {msg['content']}\n"

        full_prompt = (
            f"{system_prompt}\n\n"
            f"--- LỊCH SỬ HỘI THOẠI ---\n{history_text}\n"
            f"--- PHẢN HỒI MỚI CỦA THẦY GIÁO ---\n{user_prompt}"
        )

        try:
            model = genai.GenerativeModel(gemini_model_name)
            res = model.generate_content(
                full_prompt,
                generation_config={"temperature": 0.5, "max_output_tokens": 800},
            )
            return res.text or ""
        except Exception as primary_err:
            # Fix #1: Fallback về model đúng tên — tránh cả hai lần đều timeout
            logger.warning(
                f"Feynman primary model '{gemini_model_name}' failed: {primary_err}. "
                f"Retrying with '{_FEYNMAN_MODEL_FALLBACK}'."
            )
            try:
                model = genai.GenerativeModel(_FEYNMAN_MODEL_FALLBACK)
                res = model.generate_content(
                    full_prompt,
                    generation_config={"temperature": 0.5, "max_output_tokens": 800},
                )
                return res.text or ""
            except Exception as fallback_err:
                logger.error(f"Feynman fallback model '{_FEYNMAN_MODEL_FALLBACK}' also failed: {fallback_err}")
                return (
                    "Dạ thưa Thầy, em thấy bài học này rất thú vị! "
                    "Thầy có thể giải thích giúp em khái niệm quan trọng nhất trong bài này không ạ?"
                )

    raise RuntimeError(f"Unsupported provider: {provider}")


def start_feynman_session(
    lesson_code: str,
    enrich_summary: str,
    title: Optional[str] = "",
) -> Dict[str, Any]:
    """Start a new Feynman reverse-role session and generate the initial student query.

    Args:
        lesson_code: Lesson identifier code.
        enrich_summary: 10-minute enriched summary text of the lesson.
        title: Lesson title.

    Returns:
        Dict with session_id, initial_message, and status.
    """
    session_id = f"feynman_{uuid.uuid4().hex[:12]}"

    # Fix #3: Truncate summary để giảm token input
    truncated_summary = (enrich_summary or "Bài học tổng quan.")[:_SUMMARY_MAX_CHARS]

    FEYNMAN_SESSION_MEMORY[session_id] = []
    FEYNMAN_SESSION_LESSON[session_id] = {
        "lesson_code": lesson_code,
        "enrich_summary": truncated_summary,
        "title": title,
    }

    user_prompt = FEYNMAN_INITIAL_PROMPT.format(enrich_summary=truncated_summary)
    
    initial_msg = _call_feynman_llm(
        system_prompt=FEYNMAN_SYSTEM_PROMPT,
        history=[],
        user_prompt=user_prompt,
    )

    # Save initial AI message to session history
    FEYNMAN_SESSION_MEMORY[session_id].append({"role": "assistant", "content": initial_msg})

    return {
        "status": "success",
        "session_id": session_id,
        "lesson_code": lesson_code,
        "initial_message": initial_msg,
    }


def respond_feynman_session(
    session_id: str,
    lesson_code: str,
    student_answer: str,
    enrich_summary: Optional[str] = None,
) -> Dict[str, Any]:
    """Process student's explanation in Feynman mode and reply with next curious student query.

    Args:
        session_id: Existing Feynman chat session ID.
        lesson_code: Lesson identifier code.
        student_answer: Text response provided by student acting as teacher.
        enrich_summary: Optional summary override.

    Returns:
        Dict with session_id, reply text, and status.
    """
    if session_id not in FEYNMAN_SESSION_MEMORY:
        # Create session if expired/missing
        FEYNMAN_SESSION_MEMORY[session_id] = []
        FEYNMAN_SESSION_LESSON[session_id] = {
            "lesson_code": lesson_code,
            "enrich_summary": (enrich_summary or "")[:_SUMMARY_MAX_CHARS],
        }

    history = FEYNMAN_SESSION_MEMORY[session_id]
    lesson_info = FEYNMAN_SESSION_LESSON.get(session_id, {})

    # Fix #4: Chỉ nhúng summary vào prompt khi turn đầu tiên (history ngắn).
    summary_context = enrich_summary or lesson_info.get("enrich_summary", "")
    truncated_summary = summary_context[:_SUMMARY_MAX_CHARS]
    include_summary = len(history) <= 2  # Chỉ nhúng khi <= 1 turn đã qua

    if include_summary and truncated_summary:
        user_prompt = f"""--- THÔNG TIN NỘI DUNG BÀI GIẢNG ĐỂ THAM CHIẾU ---
{truncated_summary}

--- LỜI GIẢI THÍCH CỦA THẦY GIÁO (NGƯỜI DÙNG) ---
"{student_answer}"

Hãy đánh giá xem câu trả lời của Thầy giáo có đúng và dễ hiểu hay không, sau đó phản hồi theo đúng nguyên tắc vai trò học sinh tò mò."""
    else:
        # Từ turn 3 trở đi: prompt gọn hơn, dựa vào history để maintain context
        user_prompt = f"""--- LỜI GIẢI THÍCH MỚI CỦA THẦY GIÁO ---
"{student_answer}"

Hãy đánh giá và phản hồi theo đúng nguyên tắc vai trò học sinh tò mò."""

    reply_text = _call_feynman_llm(
        system_prompt=FEYNMAN_SYSTEM_PROMPT,
        history=history,
        user_prompt=user_prompt,
    )

    # Record exchange in session memory
    history.append({"role": "user", "content": student_answer})
    history.append({"role": "assistant", "content": reply_text})

    return {
        "status": "success",
        "session_id": session_id,
        "lesson_code": lesson_code,
        "reply": reply_text,
    }
