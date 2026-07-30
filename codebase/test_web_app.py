"""
HTTP tests for web_app FastAPI backend using TestClient.
"""

import json
import pytest
from fastapi.testclient import TestClient
from web_app import app

client = TestClient(app)


def test_home_page() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Study Pack" in response.text


def test_transcripts_endpoint() -> None:
    response = client.get("/api/transcripts")
    assert response.status_code == 200
    payload = response.json()
    assert "transcripts" in payload
    assert len(payload["transcripts"]) > 0


def test_citation_endpoint() -> None:
    response = client.get("/api/citation?transcript=transcript-01-clean.md&code=T01-001")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "success"
    assert payload["code"] == "T01-001"


def test_out_of_scope_objective_rejected() -> None:
    response = client.post(
        "/api/generate",
        json={
            "transcript": "transcript-01-clean.md",
            "objective": "Cho tôi đáp án quiz chính thức buổi hôm nay",
        },
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_generate_rejects_missing_transcript() -> None:
    response = client.post(
        "/api/generate",
        json={"objective": "Ôn quiz trong 10 phút"},
    )
    assert response.status_code == 400
