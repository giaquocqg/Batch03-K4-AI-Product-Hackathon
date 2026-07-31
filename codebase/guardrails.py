import time
import re
from typing import Dict, List, Tuple

# Rate Limiting configuration: tối đa 10 requests / 60 giây
RATE_LIMIT_WINDOW = 60  # seconds
RATE_LIMIT_MAX_REQUESTS = 10

# Lịch sử lưu timestamp của các request theo session_id/ip
# session_id -> list of float timestamps
_REQUEST_HISTORY: Dict[str, List[float]] = {}

class RateLimitExceeded(Exception):
    """Lỗi vượt quá giới hạn tần suất yêu cầu."""
    pass

def check_rate_limit(session_id: str) -> None:
    """
    Kiểm tra Rate Limit cho session_id/ip.
    Ném lỗi RateLimitExceeded nếu vượt quá giới hạn.
    """
    now = time.time()
    if session_id not in _REQUEST_HISTORY:
        _REQUEST_HISTORY[session_id] = []
        
    # Lọc bỏ các timestamp quá cũ
    history = [t for t in _REQUEST_HISTORY[session_id] if now - t < RATE_LIMIT_WINDOW]
    _REQUEST_HISTORY[session_id] = history
    
    if len(history) >= RATE_LIMIT_MAX_REQUESTS:
        time_left = int(RATE_LIMIT_WINDOW - (now - history[0]))
        raise RateLimitExceeded(f"Bạn đã hỏi quá nhanh. Vui lòng chờ {time_left} giây trước khi hỏi tiếp.")
        
    # Thêm timestamp hiện tại vào lịch sử
    _REQUEST_HISTORY[session_id].append(now)

def sanitize_chat_query(query: str) -> str:
    """
    Kiểm tra câu hỏi của học viên và lọc các ký tự độc hại,
    ngăn chặn các hình thức Prompt Injection cơ bản.
    """
    normalized = query.strip().casefold()
    
    # 1. Phát hiện các mẫu Prompt Injection nguy hiểm
    unsafe_patterns = [
        r"ignore\s+previous",
        r"bỏ\s+qua\s+chỉ\s+dẫn",
        r"bỏ\s+qua\s+quy\s+tắc",
        r"hệ\s+thống\s+bảo\s+mật",
        r"system\s+prompt",
        r"lộ\s+prompt",
        r"print\s+your\s+prompt",
        r"api\s+key",
        r"cấu\s+hình\s+hệ\s+thống"
    ]
    
    for pattern in unsafe_patterns:
        if re.search(pattern, normalized):
            raise ValueError("Phát hiện yêu cầu truy cập không an toàn. Trợ lý chỉ hỗ trợ hỏi đáp kiến thức bài học.")
            
    # 2. Ngăn chặn câu hỏi ngoài phạm vi học tập
    out_of_scope_patterns = [
        r"đáp\s+án\s+thi\s+học\s+kỳ",
        r"đáp\s+án\s+thi\s+giữa\s+kỳ",
        r"chửi",
        r"hack\s+",
        r"bẻ\s+khóa"
    ]
    
    for pattern in out_of_scope_patterns:
        if re.search(pattern, normalized):
            raise ValueError("Câu hỏi ngoài phạm vi hỗ trợ học tập của Trợ lý.")
            
    return query
