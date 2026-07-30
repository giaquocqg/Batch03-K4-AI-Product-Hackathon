"""Integrity tests for the active Paper + Day 01-05 corpus."""

import hashlib
import json
from pathlib import Path

from transcript_parser import format_segments_for_prompt, parse_transcript
from web_app import TRANSCRIPT_FILES, TRANSCRIPT_ROOT


REPO_ROOT = Path(__file__).resolve().parents[1]
CORPUS_ROOT = REPO_ROOT / "data" / "study-pack-corpus"
MANIFEST_PATH = CORPUS_ROOT / "manifest.json"
GOLDEN_SET_PATH = REPO_ROOT / "eval" / "golden_set.json"


def _manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_active_web_corpus_is_new_six_source_set_only() -> None:
    manifest = _manifest()
    expected_names = [record["file_name"] for record in manifest["files"]]

    assert TRANSCRIPT_ROOT == CORPUS_ROOT / "transcript"
    assert list(TRANSCRIPT_FILES) == expected_names
    assert expected_names == [
        "transcript-10-clean.md",
        "transcript-11-clean.md",
        "transcript-12-clean.md",
        "transcript-13-clean.md",
        "transcript-14-clean.md",
        "transcript-15-clean.md",
    ]


def test_every_active_source_segment_matches_manifest_hash_and_count() -> None:
    manifest = _manifest()
    total_segments = 0

    for record in manifest["files"]:
        path = CORPUS_ROOT / "transcript" / record["file_name"]
        transcript = parse_transcript(str(path))
        normalized_content = "\n".join(
            segment.text for segment in transcript.segments
        )
        content_hash = hashlib.sha256(
            normalized_content.encode("utf-8")
        ).hexdigest()

        assert transcript.total_segments == record["segment_count"]
        assert content_hash == record["normalized_content_sha256"]
        assert transcript.segments[0].text == record["first_segment_text"]
        assert transcript.segments[-1].text == record["last_segment_text"]
        assert transcript.segments[0].code == f"{record['transcript_id']}-001"
        assert transcript.segments[-1].code == (
            f"{record['transcript_id']}-{record['segment_count']:03d}"
        )
        total_segments += transcript.total_segments

    assert total_segments == manifest["total_segments"]
    assert total_segments == manifest["source_non_empty_lines"]


def test_longest_active_transcript_is_not_silently_truncated() -> None:
    manifest = _manifest()
    longest = max(manifest["files"], key=lambda record: record["segment_count"])
    transcript = parse_transcript(
        str(CORPUS_ROOT / "transcript" / longest["file_name"])
    )
    prompt_content = format_segments_for_prompt(transcript)

    assert f"[{transcript.segments[-1].code}]" in prompt_content
    assert "[TRUNCATED" not in prompt_content


def test_golden_set_v2_only_targets_active_corpus() -> None:
    golden_set = json.loads(GOLDEN_SET_PATH.read_text(encoding="utf-8"))
    active_names = set(TRANSCRIPT_FILES)

    assert golden_set["version"] == 2
    assert golden_set["corpus_version"] == "study-pack-corpus-v1"
    for case in golden_set["cases"]:
        transcript_name = case["input"]["transcript"]
        if transcript_name is not None:
            assert transcript_name in active_names
