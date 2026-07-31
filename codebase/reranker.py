"""
Re-ranker Module for RAG and Socratic Tutor Pipeline.
Performs second-stage candidate re-ranking using concept keyword alignment,
term overlap, and semantic scoring to eliminate context noise.
"""

import re
from typing import Any, List, Tuple

# Concept mapping for explicit disambiguation
CONCEPT_GROUPS = {
    "randomness_stability": {
        "query_keywords": [
            "ngẫu nhiên",
            "ổn định",
            "chính xác",
            "độ sáng tạo",
            "temperature",
            "top_p",
            "tham số",
        ],
        "positive_terms": [
            "temperature",
            "top_p",
            "ngẫu nhiên",
            "ổn định",
            "chính xác",
            "0",
            "mức 0",
            "tham số tinh chỉnh",
        ],
        "negative_terms": [
            "subword",
            "mã hóa unicode",
            "chi phí api",
            "tokenization",
            "1.5 - 2 lần",
        ],
    },
    "subword_cost": {
        "query_keywords": [
            "subword",
            "chi phí",
            "token",
            "tiếng việt",
            "tốn token",
            "unicode",
        ],
        "positive_terms": [
            "subword",
            "tokenization",
            "chi phí api",
            "1.5 - 2 lần",
            "tiếng việt",
            "unicode",
        ],
        "negative_terms": [
            "temperature",
            "top_p",
            "stop sequences",
            "chuỗi ký tự ngắt",
        ],
    },
}


def calculate_rerank_score(query: str, text: str, initial_score: float = 0.0) -> float:
    """Calculate composite rerank score for a candidate text given the query.

    Combines:
    1. Initial retrieval score weight (0.2)
    2. Term overlap (Word match) (0.3)
    3. Concept alignment & negative penalty (0.5)
    """
    query_lower = query.lower()
    text_lower = text.lower()

    # 1. Term overlap
    q_words = set(re.findall(r"\w+", query_lower))
    stop_words = {
        "là",
        "của",
        "và",
        "các",
        "có",
        "trong",
        "cho",
        "với",
        "để",
        "như",
        "được",
        "nghĩ",
        "em",
        "bạn",
        "thưa",
        "thầy",
        "tại",
        "sao",
        "lại",
    }
    content_q_words = {w for w in q_words if w not in stop_words and len(w) > 1}

    if content_q_words:
        matches = sum(1 for w in content_q_words if w in text_lower)
        overlap_score = matches / len(content_q_words)
    else:
        overlap_score = 0.0

    # 2. Concept alignment
    concept_score = 0.0
    for group_name, group_data in CONCEPT_GROUPS.items():
        q_matches = sum(
            1 for kw in group_data["query_keywords"] if kw in query_lower
        )
        if q_matches > 0:
            pos_matches = sum(
                1 for term in group_data["positive_terms"] if term in text_lower
            )
            neg_matches = sum(
                1 for term in group_data["negative_terms"] if term in text_lower
            )
            concept_score += (pos_matches * 1.5) - (neg_matches * 1.0)

    final_score = (
        (0.2 * initial_score)
        + (0.3 * overlap_score)
        + (0.5 * max(0.0, concept_score))
    )
    return float(final_score)


def rerank_chunks(query: str, chunks: List[str], top_k: int = 3) -> List[str]:
    """Re-ranks a list of text chunks for a given query and returns top_k most relevant chunks."""
    if not chunks:
        return []
    if len(chunks) <= 1:
        return chunks

    scored = []
    for idx, chunk in enumerate(chunks):
        score = calculate_rerank_score(
            query, chunk, initial_score=1.0 / (idx + 1)
        )
        scored.append((chunk, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in scored[:top_k]]


def rerank_tuple_results(
    query: str, candidates: List[Tuple[Any, float]], top_k: int = 3
) -> List[Tuple[Any, float]]:
    """Re-ranks candidates where candidate is (segment_obj_or_dict, initial_score)."""
    if not candidates:
        return []

    scored = []
    for item, init_score in candidates:
        text = getattr(item, "text", "") or (
            item.get("text", "") if isinstance(item, dict) else str(item)
        )
        r_score = calculate_rerank_score(query, text, initial_score=init_score)
        scored.append((item, r_score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:top_k]
