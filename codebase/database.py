import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "study_packs_db.json"

def load_db() -> dict:
    """Tải toàn bộ cơ sở dữ liệu Study Packs."""
    if not DB_PATH.exists():
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def get_study_pack_for_client(transcript_id: str) -> Optional[dict]:
    """
    Lấy Study Pack cho học viên.
    Loại bỏ trường 'correct_option' và 'explanation' để tránh học viên cheat bằng DevTools.
    """
    db = load_db()
    pack = db.get(transcript_id)
    if not pack:
        return None
    
    # Clone pack để tránh thay đổi trực tiếp db gốc
    client_pack = {
        "transcript_id": pack["transcript_id"],
        "transcript_title": pack["transcript_title"],
        "key_points": pack["key_points"],
        "keywords": pack["keywords"],
        "questions": []
    }
    
    for q in pack.get("questions", []):
        client_pack["questions"].append({
            "question": q["question"],
            "options": q["options"]
        })
        
    return client_pack

def grade_quiz(transcript_id: str, user_answers: List[str]) -> Optional[Tuple[int, List[dict], List[str]]]:
    """
    Chấm điểm bài làm của học viên.
    
    Args:
        transcript_id: Mã transcript (ví dụ T10)
        user_answers: Mảng câu trả lời của học viên (ví dụ ['A', 'B', 'C', ...])
        
    Returns:
        Tuple (score, detailed_results, weak_citations):
        - score: Điểm số trên 10
        - detailed_results: Danh sách câu hỏi kèm đáp án đúng/sai, giải thích, citation
        - weak_citations: Danh sách mã đoạn [Txx-NNN] học viên cần ôn tập lại (dựa trên các câu trả lời sai)
    """
    db = load_db()
    pack = db.get(transcript_id)
    if not pack:
        return None
    
    questions = pack.get("questions", [])
    detailed_results = []
    score = 0
    weak_citations = set()
    
    for idx, q in enumerate(questions):
        user_ans = user_answers[idx] if idx < len(user_answers) else ""
        correct_ans = q["correct_option"]
        is_correct = user_ans == correct_ans
        
        if is_correct:
            score += 1
        else:
            # Học viên sai câu này -> thêm citation của câu này vào danh sách cần ôn tập
            for cite in q.get("citations", []):
                weak_citations.add(cite)
                
        detailed_results.append({
            "question": q["question"],
            "options": q["options"],
            "user_answer": user_ans,
            "correct_option": correct_ans,
            "is_correct": is_correct,
            "explanation": q["explanation"],
            "citations": q["citations"]
        })
        
    return score, detailed_results, sorted(list(weak_citations))
