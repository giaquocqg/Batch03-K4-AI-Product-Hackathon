"""Regression tests against the supplied transcript data pack."""

from pathlib import Path

from transcript_parser import format_segments_for_prompt, parse_transcript


REPO_ROOT = Path(__file__).resolve().parents[1]
TRANSCRIPT_01 = (
    REPO_ROOT
    / 'data'
    / 'vlearn-pack'
    / 'transcript'
    / 'transcript-01-clean.md'
)
TRANSCRIPT_03 = (
    REPO_ROOT
    / 'data'
    / 'vlearn-pack'
    / 'transcript'
    / 'transcript-03-clean.md'
)


def test_parse_transcript_01_real_file() -> None:
    transcript = parse_transcript(str(TRANSCRIPT_01))

    assert transcript.transcript_id == '01'
    assert transcript.total_segments == 89
    assert transcript.segments[0].code == 'T01-001'
    assert transcript.segments[-1].code == 'T01-089'
    assert len(transcript.get_citation_codes()) == transcript.total_segments


def test_markdown_headings_are_not_citation_evidence() -> None:
    transcript = parse_transcript(str(TRANSCRIPT_01))
    segment = transcript.get_segment('T01-043')

    assert segment is not None
    assert '# Day 2' not in segment.text
    assert '## Tri thức ẩn' not in segment.text


def test_long_transcript_prompt_is_not_silently_truncated() -> None:
    transcript = parse_transcript(str(TRANSCRIPT_03))
    prompt_content = format_segments_for_prompt(transcript)
    last_lecture_segment = transcript.get_lecture_segments()[-1]

    assert transcript.total_segments == 154
    assert f'[{last_lecture_segment.code}]' in prompt_content
    assert '[TRUNCATED' not in prompt_content
