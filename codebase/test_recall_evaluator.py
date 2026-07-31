"""Tests for source-bounded semantic matching of active-recall answers."""

import json
from pathlib import Path

import pytest

import study_pack_generator as generator
from transcript_parser import parse_transcript


ACTIVE_TRANSCRIPT = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "study-pack-corpus"
    / "transcript"
    / "transcript-10-clean.md"
)


def _question() -> dict:
    return {
        "question": "Xu hướng AI chuyển dịch từ Generative AI sang Agentic AI như thế nào?",
        "answer": "Agentic AI nhấn mạnh lập kế hoạch và thực thi hành động độc lập.",
        "citations": ["T10-004"],
    }


def test_evaluator_uses_only_question_citations_and_applies_threshold(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    transcript = parse_transcript(str(ACTIVE_TRANSCRIPT))
    captured = {}

    monkeypatch.setattr(generator, "_get_api_provider", lambda: ("gemini", "test-key"))

    def fake_gemini(system: str, user: str, api_key: str, **kwargs: object) -> str:
        captured["user"] = user
        assert kwargs["response_schema"] == generator.ACTIVE_RECALL_EVALUATION_JSON_SCHEMA
        return json.dumps({
            "match_score": 72,
            "feedback": "Nêu đúng chuyển dịch trọng tâm sang hành động độc lập.",
            "evidence_citations": ["T10-004"],
        })

    monkeypatch.setattr(generator, "_call_gemini", fake_gemini)
    evaluation, metadata = generator.evaluate_active_recall_answer(
        transcript,
        _question(),
        "Agentic AI có thể lập kế hoạch và tự thực thi hành động.",
        trace_dir=str(tmp_path),
    )

    assert evaluation["match_score"] == 72
    assert evaluation["passed"] is True
    assert evaluation["threshold"] == 60
    assert metadata["evidence_citations"] == ["T10-004"]
    assert "[T10-004]" in captured["user"]
    assert "[T10-001]" not in captured["user"]


def test_evaluator_rejects_citation_outside_question_evidence(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    transcript = parse_transcript(str(ACTIVE_TRANSCRIPT))
    monkeypatch.setattr(generator, "_get_api_provider", lambda: ("gemini", "test-key"))
    monkeypatch.setattr(
        generator,
        "_call_gemini",
        lambda *args, **kwargs: json.dumps({
            "match_score": 100,
            "feedback": "Không hợp lệ.",
            "evidence_citations": ["T10-001"],
        }),
    )

    with pytest.raises(ValueError, match="citation ngoài"):
        generator.evaluate_active_recall_answer(
            transcript,
            _question(),
            "Một câu trả lời.",
            trace_dir=str(tmp_path),
        )


def test_evaluator_falls_back_to_openai_on_gemini_call_error(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    transcript = parse_transcript(str(ACTIVE_TRANSCRIPT))
    monkeypatch.setattr(
        generator,
        "_get_api_provider_candidates",
        lambda: [
            ("gemini", "test-gemini-key"),
            ("openai", "test-openai-key"),
        ],
    )
    monkeypatch.setattr(
        generator,
        "_call_gemini",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("simulated Gemini outage")
        ),
    )
    monkeypatch.setattr(
        generator,
        "_call_openai",
        lambda *args, **kwargs: json.dumps({
            "match_score": 81,
            "feedback": "Câu trả lời khớp ý trọng tâm.",
            "evidence_citations": ["T10-004"],
        }),
    )

    evaluation, metadata = generator.evaluate_active_recall_answer(
        transcript,
        _question(),
        "Agentic AI tự lập kế hoạch và thực thi hành động.",
        trace_dir=str(tmp_path),
    )

    assert evaluation["passed"] is True
    assert metadata["provider"] == "openai"
    assert metadata["fallback_used"] is True
    assert [item["status"] for item in metadata["provider_attempts"]] == [
        "api_error",
        "ok",
    ]
