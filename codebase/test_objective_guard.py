"""Scope-guard tests driven by the committed golden-set inputs."""

import json
from pathlib import Path

import pytest

from study_pack_generator import (
    SUPPORTED_OBJECTIVE,
    UnsupportedObjectiveError,
    validate_objective,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
GOLDEN_SET = REPO_ROOT / 'eval' / 'golden_set.json'


def _golden_cases() -> dict:
    data = json.loads(GOLDEN_SET.read_text(encoding='utf-8'))
    return {case['case_id']: case for case in data['cases']}


def test_supported_objective_uses_canonical_value() -> None:
    objective = _golden_cases()['GS-01']['input']['objective']

    assert validate_objective(objective) == SUPPORTED_OBJECTIVE


@pytest.mark.parametrize(
    ('case_id', 'expected_code'),
    [
        ('GS-12', 'unsupported_objective'),
        ('GS-13', 'official_answer_request'),
        ('GS-14', 'person_evaluation_request'),
        ('GS-19', 'unsafe_objective'),
        ('GS-20', 'unsafe_objective'),
    ],
)
def test_unsupported_golden_objectives_stop_before_api_call(
    case_id: str,
    expected_code: str,
) -> None:
    objective = _golden_cases()[case_id]['input']['objective']

    with pytest.raises(UnsupportedObjectiveError) as error:
        validate_objective(objective)

    assert error.value.code == expected_code
