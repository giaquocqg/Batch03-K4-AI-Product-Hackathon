"""Provider fallback and Gemini-schema compatibility tests."""

import pytest

import study_pack_generator as generator
from schema import ACTIVE_RECALL_EVALUATION_JSON_SCHEMA


def _all_keys(value: object) -> set[str]:
    keys = set()
    if isinstance(value, dict):
        keys.update(value)
        for child in value.values():
            keys.update(_all_keys(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(_all_keys(child))
    return keys


def test_gemini_schema_removes_unsupported_numeric_bounds() -> None:
    prepared = generator._prepare_gemini_schema(
        ACTIVE_RECALL_EVALUATION_JSON_SCHEMA
    )
    keys = _all_keys(prepared)

    assert "minimum" not in keys
    assert "maximum" not in keys
    assert "minLength" not in keys
    # Local validation still retains the authoritative bounds.
    score_schema = ACTIVE_RECALL_EVALUATION_JSON_SCHEMA["properties"][
        "match_score"
    ]
    assert score_schema["minimum"] == 0
    assert score_schema["maximum"] == 100


def test_openai_is_used_when_primary_gemini_call_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        generator,
        "_call_gemini",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            RuntimeError("simulated Gemini quota error")
        ),
    )
    monkeypatch.setattr(
        generator,
        "_call_openai",
        lambda *args, **kwargs: '{"status":"backup-ok"}',
    )

    raw, provider, attempts = generator._call_model_with_fallback(
        "system",
        "user",
        candidates=[
            ("gemini", "test-gemini-key"),
            ("openai", "test-openai-key"),
        ],
    )

    assert raw == '{"status":"backup-ok"}'
    assert provider == "openai"
    assert [attempt["status"] for attempt in attempts] == ["api_error", "ok"]
    assert [attempt["provider"] for attempt in attempts] == [
        "gemini",
        "openai",
    ]


def test_invalid_return_is_not_retried_as_a_provider_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    openai_called = False

    monkeypatch.setattr(
        generator,
        "_call_gemini",
        lambda *args, **kwargs: "not-json",
    )

    def fake_openai(*args, **kwargs):
        nonlocal openai_called
        openai_called = True
        return "{}"

    monkeypatch.setattr(generator, "_call_openai", fake_openai)
    raw, provider, attempts = generator._call_model_with_fallback(
        "system",
        "user",
        candidates=[
            ("gemini", "test-gemini-key"),
            ("openai", "test-openai-key"),
        ],
    )

    assert raw == "not-json"
    assert provider == "gemini"
    assert len(attempts) == 1
    assert openai_called is False


def test_all_provider_failures_are_preserved(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        generator,
        "_call_gemini",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("gemini")),
    )
    monkeypatch.setattr(
        generator,
        "_call_openai",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("openai")),
    )

    with pytest.raises(generator.AllProvidersFailedError) as error:
        generator._call_model_with_fallback(
            "system",
            "user",
            candidates=[
                ("gemini", "test-gemini-key"),
                ("openai", "test-openai-key"),
            ],
        )

    assert [attempt["provider"] for attempt in error.value.attempts] == [
        "gemini",
        "openai",
    ]
