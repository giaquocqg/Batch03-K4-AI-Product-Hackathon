#!/usr/bin/env python3
"""Mine reproducible product-demand signals from the anonymized VLearn chatlog.

The script uses explicit lexical rules only. It does not call an AI model, infer
user intent beyond those rules, or create synthetic records.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT
    / "data"
    / "vlearn-pack"
    / "chatlog"
    / "chat_history_anonymized_for_hackathon.csv"
)
DEFAULT_RESULTS = ROOT / "evidence" / "mining-results.json"
DEFAULT_AUDIT = ROOT / "evidence" / "manual-audit.csv"
DEFAULT_AUDIT_KEY = ROOT / "evidence" / "manual-audit-key.json"
DEFAULT_REVIEWER_1 = ROOT / "evidence" / "manual-audit-reviewer-1.csv"
DEFAULT_REVIEWER_2 = ROOT / "evidence" / "manual-audit-reviewer-2.csv"

SELECTED_TEXT_WRAPPER = re.compile(
    r'^\(\s*trang\s+\d+\s*,\s*đoạn được chọn\s*:\s*".*?"\s*\)\s*',
    re.IGNORECASE | re.DOTALL,
)

STUDY_PACK_PATTERNS = {
    "tom_tat": re.compile(r"\bt[oó]m\s+t[aắ]t\b", re.IGNORECASE),
    "tom_gon": re.compile(r"\bt[oó]m\s+g[oọ]n\b", re.IGNORECASE),
    "tong_hop": re.compile(r"\bt[oổ]ng\s+h[oợ]p\b", re.IGNORECASE),
    "y_chinh": re.compile(r"\b(?:[ýy]\s+ch[ií]nh|c[aá]c\s+[ýy]\s+ch[ií]nh)\b", re.IGNORECASE),
    "noi_dung_chinh": re.compile(r"\bn[oộ]i\s+dung\s+ch[ií]nh\b", re.IGNORECASE),
    "ghi_chu": re.compile(r"\bghi\s+ch[uú]\b", re.IGNORECASE),
    "note": re.compile(r"\bnotes?\b", re.IGNORECASE),
    "mindmap": re.compile(r"\bmind\s*maps?\b", re.IGNORECASE),
    "so_do_tu_duy": re.compile(r"\bs[oơ]\s+đ[oồ]\s+t[uư]\s+duy\b", re.IGNORECASE),
    "he_thong_hoa": re.compile(r"\bh[eệ]\s+th[oố]ng\s+h[oó]a\b", re.IGNORECASE),
}

RESOURCE_TERMS = re.compile(
    r"\b(?:slides?|t[aà]i\s+li[eệ]u|pdf|files?|links?)\b", re.IGNORECASE
)
RESOURCE_ACTIONS = re.compile(
    r"(?:\bt[aả]i\b|\bdownloads?\b|\bl[aấ]y\b|read_file|"
    r"kh[oô]ng\s+(?:xem|m[oở]|t[aả]i)\s+đ[uư][oợ]c|failed\s+to\s+fetch)",
    re.IGNORECASE,
)

PRACTICE_PATTERNS = {
    "request_example": re.compile(
        r"\b(?:cho|l[aấ]y|n[eê]u)\b.{0,40}\bv[ií]\s+d[uụ]\b", re.IGNORECASE | re.DOTALL
    ),
    "qualified_example": re.compile(
        r"\bv[ií]\s+d[uụ]\b.{0,30}\b(?:c[uụ]\s+th[eể]|th[uự]c\s+t[eế]|d[eễ]\s+hi[eể]u)\b",
        re.IGNORECASE | re.DOTALL,
    ),
    "use_case_request": re.compile(
        r"\bg[oợ]i\s+[ýy]\b.{0,40}\buse\s*cases?\b", re.IGNORECASE | re.DOTALL
    ),
    "lab_guidance": re.compile(
        r"\b(?:h[uư][oớ]ng\s+d[aẫ]n|b[aắ]t\s+đ[aầ]u)\b.{0,50}\b(?:labs?|th[uự]c\s+h[aà]nh)\b|"
        r"\bb[aà]i\s+labs?\b.{0,40}\b(?:l[aà]m\s+g[iì]|y[eê]u\s+c[aầ]u)\b",
        re.IGNORECASE | re.DOTALL,
    ),
}

STUDY_FAILURE_PREFIX = re.compile(
    r"^\s*(?:xin\s+l[oỗ]i|r[aấ]t\s+ti[eế]c|hi[eệ]n\s+t[aạ]i.{0,120}"
    r"(?:kh[oô]ng\s+t[iì]m|kh[oô]ng\s+th[eể]))",
    re.IGNORECASE | re.DOTALL,
)

NEAR_BOUNDARY_TERMS = re.compile(
    r"\b(?:quiz|kahoot|[oô]n\s+t[aậ]p|tr[oọ]ng\s+t[aâ]m|keyword|"
    r"ki[eế]n\s+th[uứ]c|n[oộ]i\s+dung|b[aà]i\s+h[oọ]c|slides?)\b",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--audit", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--audit-key", type=Path, default=DEFAULT_AUDIT_KEY)
    parser.add_argument("--reviewer-1", type=Path, default=DEFAULT_REVIEWER_1)
    parser.add_argument("--reviewer-2", type=Path, default=DEFAULT_REVIEWER_2)
    return parser.parse_args()


def normalize(text: str) -> str:
    return unicodedata.normalize("NFC", text or "").strip()


def clean_student_content(content: str) -> str:
    content = normalize(content)
    cleaned = SELECTED_TEXT_WRAPPER.sub("", content, count=1).strip()
    return cleaned or content


def matching_rules(text: str, patterns: dict[str, re.Pattern[str]]) -> list[str]:
    return [name for name, pattern in patterns.items() if pattern.search(text)]


def classify_study_pack(text: str) -> list[str]:
    return matching_rules(text, STUDY_PACK_PATTERNS)


def classify_course_action_hub(text: str) -> list[str]:
    if RESOURCE_TERMS.search(text) and RESOURCE_ACTIONS.search(text):
        return ["resource_and_action"]
    return []


def classify_concept_to_micro_lab(text: str) -> list[str]:
    return matching_rules(text, PRACTICE_PATTERNS)


CLASSIFIERS: dict[str, Callable[[str], list[str]]] = {
    "study_pack": classify_study_pack,
    "course_action_hub": classify_course_action_hub,
    "concept_to_micro_lab": classify_concept_to_micro_lab,
}


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def stable_order_key(turn: dict[str, object], group: str) -> str:
    raw = f"{group}:{turn['conversation_id']}:{turn['turn_id']}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def short_excerpt(text: str, limit: int = 240) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def load_turns(path: Path) -> tuple[list[dict[str, object]], dict[str, object]]:
    by_turn: dict[str, list[dict[str, str]]] = defaultdict(list)
    row_count = 0
    role_counts: Counter[str] = Counter()

    with path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        required = {
            "conversation_id",
            "user_id",
            "day_code",
            "turn_id",
            "message_id",
            "role",
            "content",
        }
        missing = required.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        for row in reader:
            row_count += 1
            role_counts[row["role"]] += 1
            by_turn[row["turn_id"]].append(row)

    turns: list[dict[str, object]] = []
    malformed_turns: list[str] = []
    for turn_id, rows in by_turn.items():
        student_rows = [row for row in rows if row["role"] == "student"]
        tutor_rows = [row for row in rows if row["role"] == "tutor"]
        if len(student_rows) != 1 or len(tutor_rows) != 1:
            malformed_turns.append(turn_id)
            continue

        student = student_rows[0]
        tutor = tutor_rows[0]
        student_content = clean_student_content(student["content"])
        labels = {name: classifier(student_content) for name, classifier in CLASSIFIERS.items()}
        turns.append(
            {
                "conversation_id": student["conversation_id"],
                "user_id": student["user_id"],
                "day_code": student["day_code"],
                "turn_id": turn_id,
                "student_content": student_content,
                "tutor_content": normalize(tutor["content"]),
                "labels": labels,
            }
        )

    validation = {
        "csv_rows": row_count,
        "role_counts": dict(sorted(role_counts.items())),
        "turn_ids_seen": len(by_turn),
        "valid_student_tutor_pairs": len(turns),
        "malformed_turn_count": len(malformed_turns),
        "malformed_turn_ids": sorted(malformed_turns),
    }
    return turns, validation


def category_summary(turns: list[dict[str, object]], category: str) -> dict[str, object]:
    matched = [turn for turn in turns if turn["labels"][category]]  # type: ignore[index]
    users = {str(turn["user_id"]) for turn in matched}
    conversations = {str(turn["conversation_id"]) for turn in matched}
    rule_counts: Counter[str] = Counter()
    for turn in matched:
        rule_counts.update(turn["labels"][category])  # type: ignore[index]

    total_turns = len(turns)
    total_users = len({str(turn["user_id"]) for turn in turns})
    total_conversations = len({str(turn["conversation_id"]) for turn in turns})
    return {
        "turns": len(matched),
        "turn_share_percent": round(len(matched) * 100 / total_turns, 2),
        "conversations": len(conversations),
        "conversation_share_percent": round(len(conversations) * 100 / total_conversations, 2),
        "users": len(users),
        "user_share_percent": round(len(users) * 100 / total_users, 2),
        "turns_per_matched_user": round(len(matched) / len(users), 2) if users else 0,
        "rule_match_counts": dict(sorted(rule_counts.items())),
    }


def build_results(
    input_path: Path, turns: list[dict[str, object]], validation: dict[str, object]
) -> dict[str, object]:
    study_turns = [turn for turn in turns if turn["labels"]["study_pack"]]  # type: ignore[index]
    heuristic_failures = [
        turn
        for turn in study_turns
        if STUDY_FAILURE_PREFIX.search(str(turn["tutor_content"])[:300])
    ]

    return {
        "methodology_version": 1,
        "source": {
            "path": input_path.relative_to(ROOT).as_posix()
            if input_path.is_relative_to(ROOT)
            else str(input_path),
            "sha256": file_sha256(input_path),
        },
        "validation": validation,
        "population": {
            "turns": len(turns),
            "conversations": len({str(turn["conversation_id"]) for turn in turns}),
            "users": len({str(turn["user_id"]) for turn in turns}),
        },
        "categories": {
            category: category_summary(turns, category) for category in CLASSIFIERS
        },
        "study_pack_tutor_failure_heuristic": {
            "definition": (
                "The first 300 characters start with xin loi, rat tiec, or a hien tai phrase "
                "followed by khong tim/khong the. This is a lexical signal, not a semantic "
                "quality judgment."
            ),
            "turns": len(heuristic_failures),
            "users": len({str(turn["user_id"]) for turn in heuristic_failures}),
            "share_of_study_pack_turns_percent": round(
                len(heuristic_failures) * 100 / len(study_turns), 2
            )
            if study_turns
            else 0,
        },
    }


def select_audit_rows(turns: list[dict[str, object]]) -> list[dict[str, object]]:
    positives = [turn for turn in turns if turn["labels"]["study_pack"]]  # type: ignore[index]
    no_study_match = [turn for turn in turns if not turn["labels"]["study_pack"]]  # type: ignore[index]
    near_boundary = [
        turn for turn in no_study_match if NEAR_BOUNDARY_TERMS.search(str(turn["student_content"]))
    ]
    boundary_ids = {str(turn["turn_id"]) for turn in near_boundary}
    negatives = [turn for turn in no_study_match if str(turn["turn_id"]) not in boundary_ids]

    groups = (
        ("rule_positive", positives, 30),
        ("near_boundary_unlabeled", near_boundary, 10),
        ("rule_negative", negatives, 20),
    )
    selected: list[dict[str, object]] = []
    for group, candidates, limit in groups:
        ordered = sorted(candidates, key=lambda turn: stable_order_key(turn, group))
        for turn in ordered[:limit]:
            selected.append({"sample_group": group, **turn})
    return selected


def write_results(path: Path, results: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as target:
        json.dump(results, target, ensure_ascii=False, indent=2, sort_keys=True)
        target.write("\n")


def write_audit(path: Path, selected: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "audit_id",
        "conversation_id",
        "turn_id",
        "day_code",
        "student_excerpt",
        "reviewer_1_label",
        "reviewer_2_label",
        "final_label",
        "review_note",
    ]
    blinded = sorted(selected, key=lambda turn: stable_order_key(turn, "blinded_audit"))
    with path.open("w", encoding="utf-8-sig", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for index, turn in enumerate(blinded, start=1):
            writer.writerow(
                {
                    "audit_id": f"A{index:03d}",
                    "conversation_id": turn["conversation_id"],
                    "turn_id": turn["turn_id"],
                    "day_code": turn["day_code"],
                    "student_excerpt": short_excerpt(str(turn["student_content"])),
                    "reviewer_1_label": "",
                    "reviewer_2_label": "",
                    "final_label": "",
                    "review_note": "",
                }
            )


def write_audit_key(path: Path, selected: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    blinded = sorted(selected, key=lambda turn: stable_order_key(turn, "blinded_audit"))
    key = {
        "warning": "Do not open this key until both reviewers have submitted independent labels.",
        "rows": [
            {
                "audit_id": f"A{index:03d}",
                "conversation_id": turn["conversation_id"],
                "turn_id": turn["turn_id"],
                "sample_group": turn["sample_group"],
                "matched_study_rules": turn["labels"]["study_pack"],  # type: ignore[index]
            }
            for index, turn in enumerate(blinded, start=1)
        ],
    }
    with path.open("w", encoding="utf-8", newline="\n") as target:
        json.dump(key, target, ensure_ascii=False, indent=2, sort_keys=True)
        target.write("\n")


def review_sheet_has_human_input(path: Path) -> bool:
    if not path.exists():
        return False
    with path.open("r", encoding="utf-8-sig", newline="") as source:
        for row in csv.DictReader(source):
            if (row.get("reviewer_label") or "").strip() or (row.get("reviewer_note") or "").strip():
                return True
    return False


def write_review_sheet(path: Path, selected: list[dict[str, object]]) -> None:
    if review_sheet_has_human_input(path):
        raise FileExistsError(
            f"Refusing to overwrite human review data in {path}. "
            "Move the completed sheet before regenerating evidence."
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "audit_id",
        "conversation_id",
        "turn_id",
        "day_code",
        "student_excerpt",
        "reviewer_label",
        "reviewer_note",
    ]
    blinded = sorted(selected, key=lambda turn: stable_order_key(turn, "blinded_audit"))
    with path.open("w", encoding="utf-8-sig", newline="") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames)
        writer.writeheader()
        for index, turn in enumerate(blinded, start=1):
            writer.writerow(
                {
                    "audit_id": f"A{index:03d}",
                    "conversation_id": turn["conversation_id"],
                    "turn_id": turn["turn_id"],
                    "day_code": turn["day_code"],
                    "student_excerpt": short_excerpt(str(turn["student_content"])),
                    "reviewer_label": "",
                    "reviewer_note": "",
                }
            )


def main() -> None:
    args = parse_args()
    input_path = args.input.resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    turns, validation = load_turns(input_path)
    results = build_results(input_path, turns, validation)
    audit_rows = select_audit_rows(turns)
    write_results(args.results.resolve(), results)
    write_audit(args.audit.resolve(), audit_rows)
    write_audit_key(args.audit_key.resolve(), audit_rows)
    write_review_sheet(args.reviewer_1.resolve(), audit_rows)
    write_review_sheet(args.reviewer_2.resolve(), audit_rows)

    print(json.dumps(results, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"Audit rows written: {len(audit_rows)}")


if __name__ == "__main__":
    main()
