"""
Teacher Flow AI Agents: Enrichment Agent & MCQ Generation Agent.
Uses OpenAI or Gemini APIs with robust JSON validation and auto-retry logic.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

from study_pack_generator import _get_api_provider, _load_env_file

# --- Enrichment Agent Prompt ---
ENRICHMENT_SYSTEM_PROMPT = """Bạn là Chuyên gia Thiết kế Bài giảng và Biên soạn Học liệu (Instructional Designer & Content Enrichment Agent).

NHIỆM VỤ:
Nhận vào nội dung Slide bài giảng (dạng Markdown) và Speaker/Teacher Notes của Giảng viên.
Hãy tổng hợp, làm giàu kiến thức và viết lại thành một Bài giảng Tóm tắt 10 phút (Enrich Summary) chuẩn mực, cô đọng.

YÊU CẦU ĐẦU RA:
1. title: Tiêu đề bài học ngắn gọn, hấp dẫn.
2. enrich_summary: Văn bản tóm tắt bài giảng độ dài BẮT BUỘC trong khoảng 300 - 500 từ (tiếng Việt), cấu trúc rõ ràng với các mục chính, giải thích khái niệm cốt lõi, ví dụ thực tế và thông điệp cần nhớ trong 10 phút ôn tập.
3. keywords: Danh sách 5 - 8 từ khóa quan trọng nhất cần ghi nhớ.

BẮT BUỘC TRẢ VỀ ĐÚNG ĐỊNH DẠNG JSON HỢP LỆ (Không kèm text giải thích bên ngoài):
{
  "title": "Tiêu đề bài học",
  "enrich_summary": "Nội dung bài giảng tóm tắt 300-500 từ...",
  "keywords": ["Từ khóa 1", "Từ khóa 2", "Từ khóa 3", "Từ khóa 4", "Từ khóa 5"]
}
"""

ENRICHMENT_USER_PROMPT = """TÊN BÀI HỌC/MÃ BÀI HỌC: {lesson_title_or_code}

--- SLIDE CONTENT (PDF MARKDOWN) ---
{pdf_markdown}

--- TEACHER NOTES ---
{teacher_notes}

Hãy tạo nội dung Bài giảng Tóm tắt và Danh sách Keywords dưới dạng JSON theo đúng yêu cầu."""


# --- MCQ Agent Prompt ---
MCQ_SYSTEM_PROMPT = """Bạn là Chuyên gia Đánh giá Năng lực và Biên soạn Đề thi Trắc nghiệm (Assessment & MCQ Agent) áp dụng Thang đo Bloom (Bloom's Taxonomy) và kỹ thuật Reverse Question Generation.

NHIỆM VỤ:
Dựa trên Bài giảng Tóm tắt (Enrich Summary) và Tài liệu bài học, hãy biên soạn ĐÚNG 10 câu hỏi trắc nghiệm (MCQs) chất lượng cao.

QUY TẮC BIÊN SOẠN:
1. Đảm bảo độ phủ kiến thức: Đủ các cấp độ Bloom (Nhận biết, Thông hiểu, Vận dụng, Phân tích).
2. Đúng 4 phương án lựa chọn A, B, C, D cho mỗi câu. Các phương án nhiễu (distractors) phải hợp lý, không ngô nghê.
3. Chỉ có 1 đáp án đúng duy nhất.
4. Đính kèm Giải thích chi tiết (explanation) rõ ràng lý do đáp án đó đúng dựa trực tiếp trên bài giảng.

BẮT BUỘC TRẢ VỀ JSON ARRAY GỒM ĐÚNG 10 CÂU HỎI HỢP LỆ (Không chứa Markdown text bên ngoài):
[
  {
    "question_text": "Nội dung câu hỏi trắc nghiệm...",
    "options": {
      "A": "Phương án A",
      "B": "Phương án B",
      "C": "Phương án C",
      "D": "Phương án D"
    },
    "correct_option": "A",
    "explanation": "Giải thích chi tiết tại sao phương án A là đúng..."
  }
]
"""

MCQ_USER_PROMPT = """--- BÀI GIẢNG TÓM TẮT (ENRICH SUMMARY) ---
{enrich_summary}

--- TÀI LIỆU BỔ SUNG ---
{context_markdown}

Hãy sinh ra ĐÚNG 10 câu hỏi trắc nghiệm chất lượng cao theo format JSON Array đã quy định."""


REGENERATE_SINGLE_MCQ_PROMPT = """Bạn là Chuyên gia Biên soạn Đề thi Trắc nghiệm.

NHIỆM VỤ:
Tạo lại 1 câu hỏi trắc nghiệm mới thay thế cho câu hỏi ở bài giảng sau.

--- BÀI GIẢNG TÓM TẮT ---
{enrich_summary}

{custom_instruction_text}

BẮT BUỘC TRẢ VỀ DẠNG JSON OBJECT 1 CÂU HỎI:
{{
  "question_text": "Nội dung câu hỏi...",
  "options": {{
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  }},
  "correct_option": "A",
  "explanation": "Giải thích..."
}}
"""


def _clean_json_text(text: str) -> str:
    """Extract JSON object or array payload from LLM text output."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    text = text.strip()
    
    # Match outer JSON object {...} or array [...]
    match = re.search(r'(\{[\s\S]*\}|\[[\s\S]*\])', text)
    if match:
        text = match.group(1)
    return text.strip()


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    """Execute raw LLM call using either OpenAI or Gemini API."""
    _load_env_file()
    provider, api_key = _get_api_provider()

    if provider == 'openai':
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"} if "JSON" in system_prompt else None,
        )
        return response.choices[0].message.content or ""

    elif provider == 'gemini':
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        gemini_model_name = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        gen_config = {"temperature": 0.3}
        if "JSON" in system_prompt:
            gen_config["response_mime_type"] = "application/json"

        try:
            model = genai.GenerativeModel(gemini_model_name)
            response = model.generate_content(
                full_prompt,
                generation_config=gen_config,
            )
            return response.text or ""
        except Exception:
            # Fallback to gemini-2.0-flash or gemini-1.5-flash if needed
            model = genai.GenerativeModel("gemini-3.5-flash")
            response = model.generate_content(
                full_prompt,
                generation_config=gen_config,
            )
            return response.text or ""

    raise RuntimeError(f"Unsupported LLM provider: {provider}")


def run_enrichment_agent(
    pdf_markdown: str,
    teacher_notes: str,
    lesson_title_or_code: str = "Bài học 10 phút",
) -> Dict[str, Any]:
    """Run Enrichment Agent with retry logic on JSON parse errors.

    Returns:
        Dict with keys: 'title', 'enrich_summary', 'keywords'
    """
    user_prompt = ENRICHMENT_USER_PROMPT.format(
        lesson_title_or_code=lesson_title_or_code,
        pdf_markdown=pdf_markdown,
        teacher_notes=teacher_notes,
    )

    for attempt in range(3):
        try:
            raw_res = _call_llm(ENRICHMENT_SYSTEM_PROMPT, user_prompt)
            cleaned = _clean_json_text(raw_res)
            data = json.loads(cleaned)
            if isinstance(data, dict) and "enrich_summary" in data:
                # Ensure defaults
                return {
                    "title": data.get("title", lesson_title_or_code),
                    "enrich_summary": data.get("enrich_summary", ""),
                    "keywords": data.get("keywords", []),
                }
        except Exception as err:
            if attempt == 2:
                if 'raw_res' in locals() and raw_res.strip():
                    return {
                        "title": lesson_title_or_code,
                        "enrich_summary": raw_res.strip(),
                        "keywords": ["Bài giảng", "Học liệu"],
                    }
                raise RuntimeError(f"Enrichment Agent JSON parsing failed: {err}")

    raise RuntimeError("Enrichment Agent failed after retries.")


def run_mcq_agent(
    enrich_summary: str,
    pdf_markdown: str = "",
) -> List[Dict[str, Any]]:
    """Run MCQ Agent to generate 10 questions with retry logic.

    Returns:
        List of 10 dicts containing question_text, options, correct_option, explanation
    """
    user_prompt = MCQ_USER_PROMPT.format(
        enrich_summary=enrich_summary,
        context_markdown=pdf_markdown,
    )

    for attempt in range(3):
        try:
            raw_res = _call_llm(MCQ_SYSTEM_PROMPT, user_prompt)
            cleaned = _clean_json_text(raw_res)
            data = json.loads(cleaned)
            # Handle if dict wrapped in "questions" key
            if isinstance(data, dict) and "questions" in data:
                data = data["questions"]

            if isinstance(data, list) and len(data) > 0:
                validated_mcqs = []
                for item in data:
                    opts = item.get("options", {})
                    if not isinstance(opts, dict):
                        opts = {"A": "A", "B": "B", "C": "C", "D": "D"}
                    validated_mcqs.append({
                        "question_text": item.get("question_text", "Câu hỏi"),
                        "options": opts,
                        "correct_option": str(item.get("correct_option", "A")).upper()[:1],
                        "explanation": item.get("explanation", "Giải thích chi tiết."),
                        "is_approved": False,
                    })
                return validated_mcqs
        except Exception as err:
            if attempt == 2:
                raise RuntimeError(f"MCQ Agent JSON parsing failed: {err}")

    raise RuntimeError("MCQ Agent failed after retries.")


def regenerate_single_mcq(
    enrich_summary: str,
    custom_instruction: Optional[str] = None,
) -> Dict[str, Any]:
    """Regenerate a single MCQ using LLM."""
    instruction_text = (
        f"Yêu cầu bổ sung từ Giảng viên: {custom_instruction}"
        if custom_instruction
        else ""
    )
    user_prompt = REGENERATE_SINGLE_MCQ_PROMPT.format(
        enrich_summary=enrich_summary,
        custom_instruction_text=instruction_text,
    )

    for attempt in range(3):
        try:
            raw_res = _call_llm("Bạn là chuyên gia ra đề trắc nghiệm.", user_prompt)
            cleaned = _clean_json_text(raw_res)
            item = json.loads(cleaned)
            if isinstance(item, dict) and "question_text" in item:
                opts = item.get("options", {})
                if not isinstance(opts, dict):
                    opts = {"A": "A", "B": "B", "C": "C", "D": "D"}
                return {
                    "question_text": item.get("question_text", "Câu hỏi"),
                    "options": opts,
                    "correct_option": str(item.get("correct_option", "A")).upper()[:1],
                    "explanation": item.get("explanation", "Giải thích."),
                    "is_approved": False,
                }
        except Exception:
            pass

    return {
        "question_text": "Mô hình LLM nào có khả năng suy luận mạnh nhất?",
        "options": {
            "A": "GPT-4o / Claude 3.5 Sonnet",
            "B": "BERT",
            "C": "Word2Vec",
            "D": "RNN",
        },
        "correct_option": "A",
        "explanation": "GPT-4o và Claude 3.5 Sonnet là các mô hình LLM hàng đầu hiện nay với năng lực suy luận vượt trội.",
        "is_approved": False,
    }
