"""HITL review tests derived from the real active transcript corpus."""

from copy import deepcopy
from pathlib import Path

import pytest

from review_store import (
    ReviewConflictError,
    ReviewNotFoundError,
    ReviewValidationError,
    approve_review_draft,
    create_review_draft,
    get_review_draft,
    update_review_draft,
)
from transcript_parser import parse_transcript


REPO_ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPT_PATH = (
    REPO_ROOT
    / "data"
    / "study-pack-corpus"
    / "transcript"
    / "transcript-10-clean.md"
)


def _source_derived_pack(question_count: int = 2) -> tuple[object, dict]:
    transcript = parse_transcript(str(TRANSCRIPT_PATH))
    segments = transcript.get_lecture_segments()
    pack = {
        "key_points": [
            {
                "content": segments[0].text,
                "citations": [segments[0].code],
            }
        ],
        "keywords": [segments[0].text.split()[0]],
        "questions": [
            {
                "question": f"Giải thích nội dung của đoạn {segment.code}.",
                "answer": segment.text,
                "citations": [segment.code],
            }
            for segment in segments[1:1 + question_count]
        ],
    }
    return transcript, pack


def test_review_draft_can_be_saved_and_approved(tmp_path: Path) -> None:
    transcript, pack = _source_derived_pack()
    review = create_review_draft(
        review_dir=str(tmp_path),
        transcript_name=TRANSCRIPT_PATH.name,
        transcript=transcript,
        study_pack=pack,
        objective="Ôn quiz trong 10 phút",
        generation_trace_id="real-trace-reference",
    )

    edited = deepcopy(pack)
    edited["questions"][0]["question"] += " Trả lời bằng lời của bạn."
    saved = update_review_draft(
        review_dir=str(tmp_path),
        draft_id=review["draft_id"],
        transcript=transcript,
        study_pack=edited,
        expected_revision=review["revision"],
        action="question_edited",
    )
    approved = approve_review_draft(
        review_dir=str(tmp_path),
        draft_id=review["draft_id"],
        transcript=transcript,
        study_pack=edited,
        expected_revision=saved["revision"],
    )

    assert approved["status"] == "approved"
    assert approved["revision"] == 3
    assert get_review_draft(
        str(tmp_path), review["draft_id"]
    )["study_pack"] == edited


def test_review_rejects_invalid_citation(tmp_path: Path) -> None:
    transcript, pack = _source_derived_pack()
    review = create_review_draft(
        str(tmp_path),
        TRANSCRIPT_PATH.name,
        transcript,
        pack,
        "Ôn quiz trong 10 phút",
        "real-trace-reference",
    )
    pack["questions"][0]["citations"] = ["T99-999"]

    with pytest.raises(ReviewValidationError) as error:
        update_review_draft(
            str(tmp_path),
            review["draft_id"],
            transcript,
            pack,
            review["revision"],
        )

    assert error.value.validation["invalid_citations"] == ["T99-999"]


def test_review_rejects_stale_revision_and_incomplete_approval(
    tmp_path: Path,
) -> None:
    transcript, pack = _source_derived_pack()
    review = create_review_draft(
        str(tmp_path),
        TRANSCRIPT_PATH.name,
        transcript,
        pack,
        "Ôn quiz trong 10 phút",
        "real-trace-reference",
    )
    saved = update_review_draft(
        str(tmp_path),
        review["draft_id"],
        transcript,
        pack,
        review["revision"],
    )

    with pytest.raises(ReviewConflictError):
        update_review_draft(
            str(tmp_path),
            review["draft_id"],
            transcript,
            pack,
            review["revision"],
        )

    incomplete = deepcopy(pack)
    incomplete["questions"].pop()
    with pytest.raises(ReviewValidationError, match="Cần đủ 2 câu"):
        approve_review_draft(
            str(tmp_path),
            review["draft_id"],
            transcript,
            incomplete,
            saved["revision"],
        )


def test_review_id_cannot_escape_review_directory(tmp_path: Path) -> None:
    with pytest.raises(ReviewNotFoundError):
        get_review_draft(str(tmp_path), "review_../../outside")
