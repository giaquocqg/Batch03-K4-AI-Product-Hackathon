"""
Transcript parser for VLearn lecture transcripts.

Parses clean transcript markdown files into structured segments
with citation IDs [Txx-NNN] for use in Study Pack generation.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

# Pattern matches: **[T01-001]** or **[T01-001]** at start of paragraph
CITATION_PATTERN = re.compile(
    r'^\*\*\[(?P<code>T\d{2}-\d{3})\]\*\*\s*(?P<text>.+)',
    re.DOTALL
)

# Pattern to detect [không nghe rõ] markers
UNCLEAR_MARKER = re.compile(r'\[không nghe rõ\]', re.IGNORECASE)

# Pattern to detect [Hoạt động lớp: ...] markers (collapsed class activities)
CLASS_ACTIVITY_PATTERN = re.compile(r'\[Hoạt động lớp:.*?\]', re.DOTALL)

# Markdown headings delimit sections but are not transcript evidence.
MARKDOWN_HEADING_PATTERN = re.compile(r'^#{1,6}\s+')


@dataclass
class TranscriptSegment:
    """A single paragraph/segment from a transcript."""
    code: str           # e.g., "T01-005"
    text: str           # Full text content of the segment
    has_unclear: bool   # Contains [không nghe rõ] markers
    is_activity: bool   # Is a class activity note (not lecture content)
    line_number: int    # Line number in source file


@dataclass
class ParsedTranscript:
    """Complete parsed transcript with metadata."""
    file_path: str
    title: str
    transcript_id: str   # e.g., "01" from transcript-01-clean.md
    segments: List[TranscriptSegment]
    total_segments: int
    unclear_count: int
    unclear_marker_count: int
    activity_count: int

    def get_segment(self, code: str) -> Optional[TranscriptSegment]:
        """Look up a segment by its citation code."""
        for seg in self.segments:
            if seg.code == code:
                return seg
        return None

    def get_citation_codes(self) -> set:
        """Return all valid citation codes in this transcript."""
        return {seg.code for seg in self.segments}

    def get_lecture_segments(self) -> List[TranscriptSegment]:
        """Return only lecture content segments (exclude class activities)."""
        return [seg for seg in self.segments if not seg.is_activity]

    def get_lecture_citation_codes(self) -> set:
        """Return citation codes that are included in the model prompt."""
        return {seg.code for seg in self.get_lecture_segments()}


def extract_transcript_id(file_path: str) -> str:
    """Extract transcript number from filename.

    Example: 'transcript-01-clean.md' -> '01'
    """
    match = re.search(r'transcript-(\d{2})-clean', Path(file_path).name)
    if match:
        return match.group(1)
    raise ValueError(
        f"Cannot extract transcript ID from filename: {file_path}. "
        f"Expected format: transcript-XX-clean.md"
    )


def extract_title(content: str) -> str:
    """Extract the title from the first markdown heading."""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            return line[2:].strip()
    return "(Không có tiêu đề)"


def parse_transcript(file_path: str) -> ParsedTranscript:
    """Parse a clean transcript markdown file into structured segments.

    Args:
        file_path: Path to transcript-XX-clean.md file.

    Returns:
        ParsedTranscript with all segments, metadata, and lookup methods.

    Raises:
        FileNotFoundError: If file does not exist.
        ValueError: If file does not contain any valid segments.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Transcript file not found: {file_path}")

    content = path.read_text(encoding='utf-8')
    transcript_id = extract_transcript_id(file_path)
    title = extract_title(content)

    segments: List[TranscriptSegment] = []
    lines = content.split('\n')

    # Accumulate multi-line paragraphs.
    current_code = None
    current_text_lines = []
    current_line_number = 0

    def save_current_segment() -> None:
        nonlocal current_code, current_text_lines, current_line_number
        if current_code is None:
            return

        full_text = ' '.join(current_text_lines).strip()
        segments.append(TranscriptSegment(
            code=current_code,
            text=full_text,
            has_unclear=bool(UNCLEAR_MARKER.search(full_text)),
            is_activity=bool(CLASS_ACTIVITY_PATTERN.search(full_text)),
            line_number=current_line_number,
        ))
        current_code = None
        current_text_lines = []
        current_line_number = 0

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        match = CITATION_PATTERN.match(stripped)

        if match:
            save_current_segment()

            # Start new segment
            current_code = match.group('code')
            current_text_lines = [match.group('text').strip()]
            current_line_number = i

        elif MARKDOWN_HEADING_PATTERN.match(stripped):
            save_current_segment()

        elif current_code is not None and stripped:
            # Continue accumulating text for current segment
            current_text_lines.append(stripped)

    # Save last segment
    save_current_segment()

    if not segments:
        raise ValueError(
            f"No valid segments found in {file_path}. "
            f"Expected paragraphs starting with **[Txx-NNN]**"
        )

    codes = [segment.code for segment in segments]
    if len(codes) != len(set(codes)):
        duplicate_codes = sorted({code for code in codes if codes.count(code) > 1})
        raise ValueError(
            f"Duplicate citation codes in {file_path}: {duplicate_codes}"
        )

    expected_prefix = f"T{transcript_id}-"
    mismatched_codes = [code for code in codes if not code.startswith(expected_prefix)]
    if mismatched_codes:
        raise ValueError(
            f"Citation codes do not match transcript {transcript_id}: "
            f"{mismatched_codes}"
        )

    unclear_count = sum(1 for seg in segments if seg.has_unclear)
    unclear_marker_count = sum(
        len(UNCLEAR_MARKER.findall(segment.text)) for segment in segments
    )
    activity_count = sum(1 for seg in segments if seg.is_activity)

    return ParsedTranscript(
        file_path=str(path.resolve()),
        title=title,
        transcript_id=transcript_id,
        segments=segments,
        total_segments=len(segments),
        unclear_count=unclear_count,
        unclear_marker_count=unclear_marker_count,
        activity_count=activity_count,
    )


def format_segments_for_prompt(
    transcript: ParsedTranscript,
    exclude_activities: bool = True,
    max_chars: Optional[int] = None,
) -> str:
    """Format transcript segments into a string suitable for LLM prompt.

    Args:
        transcript: Parsed transcript object.
        exclude_activities: If True, skip class activity segments.
        max_chars: Optional maximum total characters. Raises instead of silently
            truncating evidence when the limit is exceeded.

    Returns:
        Formatted string with [Txx-NNN] labels and text.
    """
    parts = []
    total_chars = 0

    segments = (
        transcript.get_lecture_segments()
        if exclude_activities
        else transcript.segments
    )

    for seg in segments:
        entry = f"[{seg.code}] {seg.text}"
        if max_chars is not None and total_chars + len(entry) > max_chars:
            raise ValueError(
                f"Transcript prompt exceeds max_chars={max_chars} before "
                f"segment {seg.code}; no evidence was silently truncated."
            )
        parts.append(entry)
        total_chars += len(entry) + 2

    return '\n\n'.join(parts)


# --- CLI usage for testing ---
if __name__ == '__main__':
    import sys

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 2:
        print("Usage: python transcript_parser.py <path-to-transcript.md>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = parse_transcript(file_path)

    print(f"Transcript: {result.title}")
    print(f"ID: T{result.transcript_id}")
    print(f"Total segments: {result.total_segments}")
    print(f"  Lecture content: {result.total_segments - result.activity_count}")
    print(f"  Class activities: {result.activity_count}")
    print(f"  Segments with [không nghe rõ]: {result.unclear_count}")
    print(f"  [không nghe rõ] markers: {result.unclear_marker_count}")
    print(f"  Citation codes: {sorted(result.get_citation_codes())[:5]}...")
    print()
    print("First 3 lecture segments:")
    for seg in result.get_lecture_segments()[:3]:
        preview = seg.text[:150] + "..." if len(seg.text) > 150 else seg.text
        print(f"  [{seg.code}] {preview}")
