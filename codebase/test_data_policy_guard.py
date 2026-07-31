"""External-provider policy gates must run before protected data upload."""

import pytest

from study_pack_generator import (
    DataPolicyNotConfirmedError,
    _get_api_provider,
)


def _clear_provider_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "GOOGLE_API_KEY",
        "OPENAI_API_KEY",
        "LLM_PROVIDER",
        "PROVIDER",
        "EXTERNAL_AI_DATA_POLICY_CONFIRMED",
    ):
        monkeypatch.delenv(name, raising=False)


def test_external_provider_requires_explicit_policy_confirmation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_provider_environment(monkeypatch)
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-non-secret-value")
    monkeypatch.setenv("LLM_PROVIDER", "openai")

    with pytest.raises(DataPolicyNotConfirmedError):
        _get_api_provider()


def test_confirmed_gemini_configuration_is_selected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_provider_environment(monkeypatch)
    monkeypatch.setenv("GOOGLE_API_KEY", "test-only-non-secret-value")
    monkeypatch.setenv("LLM_PROVIDER", "gemini")
    monkeypatch.setenv("EXTERNAL_AI_DATA_POLICY_CONFIRMED", "true")
    assert _get_api_provider() == (
        "gemini",
        "test-only-non-secret-value",
    )
