"""
Unit tests for Reranker module and Database Inspector endpoint.
"""

import pytest
from fastapi.testclient import TestClient

from reranker import calculate_rerank_score, rerank_chunks, rerank_tuple_results
from inspect_db import get_db_summary_dict, inspect_sqlite, inspect_chromadb
from web_app import app

client = TestClient(app)

def test_reranker_concept_disambiguation():
    """Verify Reranker correctly ranks Temperature chunk above Subword chunk for a stability query."""
    query = "Tại sao tham số lại làm tăng tính ổn định, ít ngẫu nhiên trong câu trả lời?"
    
    subword_chunk = (
        "Tokenization chia nhỏ văn bản thành các phân đoạn subword. "
        "Trung bình 1 token tương đương 0.75 từ tiếng Anh, nhưng chỉ 0.5 từ tiếng Việt. "
        "Chi phí API call tiếng Việt tăng gấp 1.5 - 2 lần."
    )
    
    temperature_chunk = (
        "Temperature (Độ sáng tạo/Độ ngẫu nhiên): Nhận giá trị từ 0 đến 1. "
        "Thiết lập mức 0 cho các tác vụ đòi hỏi sự ổn định, chính xác tuyệt đối như viết code hoặc phân tích tài chính."
    )
    
    chunks = [subword_chunk, temperature_chunk]
    reranked = rerank_chunks(query, chunks, top_k=2)
    
    # Temperature chunk must be ranked #1
    assert len(reranked) == 2
    assert "Temperature" in reranked[0]
    assert "subword" in reranked[1].lower()


def test_reranker_tuple_results():
    """Verify rerank_tuple_results works with object tuples."""
    class DummySeg:
        def __init__(self, text):
            self.text = text

    seg1 = DummySeg("Chi phí API subword tokenization tiếng Việt tăng gấp 2 lần")
    seg2 = DummySeg("Temperature thiết lập mức 0 cho tác vụ ổn định, ít ngẫu nhiên")
    
    candidates = [(seg1, 0.9), (seg2, 0.8)]
    query = "Làm thế nào để kết quả trả về ít ngẫu nhiên và ổn định nhất?"
    
    reranked = rerank_tuple_results(query, candidates, top_k=2)
    assert reranked[0][0].text == seg2.text


def test_db_inspect_summary():
    """Verify DB Inspector dictionary output."""
    summary = get_db_summary_dict()
    assert "sqlite" in summary
    assert "chromadb" in summary
    assert "lessons_count" in summary["sqlite"]
    assert "questions_count" in summary["sqlite"]


def test_db_inspect_api_endpoint():
    """Verify GET /api/admin/db-inspect endpoint."""
    response = client.get("/api/admin/db-inspect")
    assert response.status_code == 200
    data = response.json()
    assert "sqlite" in data
    assert "chromadb" in data
