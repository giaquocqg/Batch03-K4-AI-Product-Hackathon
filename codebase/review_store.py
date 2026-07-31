"""Persistent teacher-review drafts and audit logs for the HITL flow."""

from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import threading
from typing import Optional
from uuid import uuid4

from citation_validator import validate_citations
from schema import validate_study_pack_output
from transcript_parser import ParsedTranscript


REVIEW_METHOD_VERSION = "teacher-review-v1"
_STORE_LOCK = threading.RLock()
_DRAFT_ID_PATTERN = re.compile(r"^review_[0-9a-f]{32}$")


class ReviewNotFoundError(LookupError):
    """Raised when a requested draft does not exist."""


class ReviewConflictError(RuntimeError):
    """Raised when a stale revision or approved draft is modified."""


class ReviewValidationError(ValueError):
    """Raised when teacher changes cannot be safely saved or approved."""

    def __init__(self, message: str, validation: Optional[dict] = None):
        super().__init__(message)
        self.validation = validation


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _review_path(review_dir: str, draft_id: str) -> Path:
    if (
        not isinstance(draft_id, str)
        or _DRAFT_ID_PATTERN.fullmatch(draft_id) is None
    ):
        raise ReviewNotFoundError("Không tìm thấy bản nháp review.")
    return Path(review_dir) / f"{draft_id}.json"


def _write_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = path.with_suffix(".tmp")
    temporary_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temporary_path.replace(path)


def _read_record(review_dir: str, draft_id: str) -> tuple[Path, dict]:
    path = _review_path(review_dir, draft_id)
    if not path.is_file():
        raise ReviewNotFoundError("Không tìm thấy bản nháp review.")
    try:
        record = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReviewValidationError(
            "Không thể đọc bản nháp review đã lưu."
        ) from error
    return path, record


def _validate_pack(pack: object, transcript: ParsedTranscript) -> dict:
    try:
        validate_study_pack_output(pack)
    except ValueError as error:
        raise ReviewValidationError(str(error)) from error
    validation = validate_citations(pack, transcript)
    if not validation["valid"]:
        raise ReviewValidationError(
            "Bản nháp có citation thiếu, không tồn tại, hoặc chỉ dựa trên "
            "đoạn [không nghe rõ].",
            validation,
        )
    return validation


def _public_record(record: dict) -> dict:
    return {
        key: deepcopy(record[key])
        for key in (
            "draft_id",
            "status",
            "revision",
            "required_questions",
            "study_pack",
            "validation",
            "transcript",
            "created_at",
            "updated_at",
            "approved_at",
        )
        if key in record
    }


def create_review_draft(
    review_dir: str,
    transcript_name: str,
    transcript: ParsedTranscript,
    study_pack: dict,
    objective: str,
    generation_trace_id: str,
) -> dict:
    """Create a reviewable copy of a real generated Study Pack."""
    validation = _validate_pack(study_pack, transcript)
    timestamp = _now()
    draft_id = f"review_{uuid4().hex}"
    record = {
        "draft_id": draft_id,
        "method_version": REVIEW_METHOD_VERSION,
        "status": "draft",
        "revision": 1,
        "required_questions": len(study_pack["questions"]),
        "objective": objective,
        "generation_trace_id": generation_trace_id,
        "transcript": {
            "file_name": transcript_name,
            "transcript_id": f"T{transcript.transcript_id}",
            "title": transcript.title,
        },
        "original_study_pack": deepcopy(study_pack),
        "study_pack": deepcopy(study_pack),
        "validation": validation,
        "created_at": timestamp,
        "updated_at": timestamp,
        "approved_at": None,
        "audit_log": [
            {
                "timestamp": timestamp,
                "actor": "teacher",
                "action": "draft_created_from_generation",
                "revision": 1,
                "details": {"generation_trace_id": generation_trace_id},
            }
        ],
    }
    with _STORE_LOCK:
        _write_record(_review_path(review_dir, draft_id), record)
    return _public_record(record)


def get_review_draft(review_dir: str, draft_id: str) -> dict:
    """Return the current public state of a review draft."""
    with _STORE_LOCK:
        _, record = _read_record(review_dir, draft_id)
    return _public_record(record)


def update_review_draft(
    review_dir: str,
    draft_id: str,
    transcript: ParsedTranscript,
    study_pack: dict,
    expected_revision: int,
    action: str = "draft_saved",
    details: Optional[dict] = None,
) -> dict:
    """Validate and persist teacher changes using optimistic concurrency."""
    validation = _validate_pack(study_pack, transcript)
    if not isinstance(action, str) or not action.strip():
        action = "draft_saved"
    safe_details = details if isinstance(details, dict) else {}

    with _STORE_LOCK:
        path, record = _read_record(review_dir, draft_id)
        if record["status"] == "approved":
            raise ReviewConflictError(
                "Study Pack đã được phê duyệt và đang ở chế độ chỉ đọc."
            )
        if expected_revision != record["revision"]:
            raise ReviewConflictError(
                "Bản nháp đã thay đổi ở nơi khác. Hãy tải lại trước khi lưu."
            )
        if (
            record["transcript"]["transcript_id"]
            != f"T{transcript.transcript_id}"
        ):
            raise ReviewValidationError(
                "Transcript của bản nháp không khớp nguồn đang kiểm tra."
            )

        timestamp = _now()
        record["revision"] += 1
        record["study_pack"] = deepcopy(study_pack)
        record["validation"] = validation
        record["updated_at"] = timestamp
        record["audit_log"].append(
            {
                "timestamp": timestamp,
                "actor": "teacher",
                "action": action[:80],
                "revision": record["revision"],
                "details": safe_details,
            }
        )
        _write_record(path, record)
    return _public_record(record)


def approve_review_draft(
    review_dir: str,
    draft_id: str,
    transcript: ParsedTranscript,
    study_pack: dict,
    expected_revision: int,
) -> dict:
    """Approve only a complete, citation-valid teacher-reviewed pack."""
    validation = _validate_pack(study_pack, transcript)

    with _STORE_LOCK:
        path, record = _read_record(review_dir, draft_id)
        if record["status"] == "approved":
            return _public_record(record)
        if expected_revision != record["revision"]:
            raise ReviewConflictError(
                "Bản nháp đã thay đổi ở nơi khác. Hãy tải lại trước khi duyệt."
            )
        question_count = len(study_pack["questions"])
        if question_count != record["required_questions"]:
            raise ReviewValidationError(
                f"Cần đủ {record['required_questions']} câu trước khi phê duyệt; "
                f"hiện có {question_count}.",
                validation,
            )

        timestamp = _now()
        record["revision"] += 1
        record["status"] = "approved"
        record["study_pack"] = deepcopy(study_pack)
        record["validation"] = validation
        record["updated_at"] = timestamp
        record["approved_at"] = timestamp
        record["audit_log"].append(
            {
                "timestamp": timestamp,
                "actor": "teacher",
                "action": "study_pack_approved",
                "revision": record["revision"],
                "details": {"question_count": question_count},
            }
        )
        _write_record(path, record)
    return _public_record(record)
