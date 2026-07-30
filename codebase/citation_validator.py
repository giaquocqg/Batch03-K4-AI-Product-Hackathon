"""
Citation validator for Study Pack outputs.

Validates that all citation codes in an LLM-generated Study Pack
actually exist in the source transcript. This is a deterministic check —
it verifies syntactic validity, not semantic groundedness.
"""

import re
from typing import Dict, List, Set, Tuple

from transcript_parser import ParsedTranscript

# Pattern to extract citation codes from LLM output
CITATION_CODE_PATTERN = re.compile(r'T\d{2}-\d{3}')


def extract_citations_from_output(output: dict) -> Set[str]:
    """Extract all citation codes from a Study Pack JSON output.

    Traverses key_points[].citations and questions[].citations.

    Args:
        output: Parsed JSON output from LLM.

    Returns:
        Set of all citation codes found in the output.
    """
    codes = set()

    for kp in output.get('key_points', []):
        for cite in kp.get('citations', []):
            if isinstance(cite, str):
                codes.add(cite)

    for q in output.get('questions', []):
        for cite in q.get('citations', []):
            if isinstance(cite, str):
                codes.add(cite)

    return codes


def _citation_occurrences(output: dict) -> List[str]:
    """Return citation uses without deduplicating repeated codes."""
    citations = []
    for item_type in ('key_points', 'questions'):
        for item in output.get(item_type, []):
            item_citations = item.get('citations', [])
            if isinstance(item_citations, list):
                citations.extend(
                    citation for citation in item_citations
                    if isinstance(citation, str)
                )
    return citations


def validate_citations(
    output: dict,
    transcript: ParsedTranscript,
) -> Dict[str, object]:
    """Validate all citations in a Study Pack output against the transcript.

    Args:
        output: Parsed JSON output from LLM.
        transcript: Parsed transcript used as source.

    Returns:
        Validation result dict with:
        - valid: bool — True if ALL citations are valid
        - total_citations: int
        - valid_citations: list of valid codes
        - invalid_citations: list of codes not found in transcript
        - unclear_citations: list of codes pointing to segments with [không nghe rõ]
        - validity_rate: float (0.0 to 1.0)
    """
    output_codes = extract_citations_from_output(output)
    occurrences = _citation_occurrences(output)
    transcript_codes = transcript.get_lecture_citation_codes()

    valid_codes = []
    invalid_codes = []
    unclear_codes = []

    for code in sorted(output_codes):
        if code not in transcript_codes:
            invalid_codes.append(code)
        else:
            valid_codes.append(code)
            segment = transcript.get_segment(code)
            if segment and segment.has_unclear:
                unclear_codes.append(code)

    missing_citation_items = []
    unclear_only_items = []
    for item_type in ('key_points', 'questions'):
        for index, item in enumerate(output.get(item_type, [])):
            citations = item.get('citations', [])
            if not isinstance(citations, list) or not citations:
                missing_citation_items.append(f"{item_type}[{index}]")
                continue
            segments = [
                transcript.get_segment(citation)
                for citation in citations
                if isinstance(citation, str) and citation in transcript_codes
            ]
            if segments and len(segments) == len(citations) and all(
                segment.has_unclear for segment in segments
            ):
                unclear_only_items.append(f"{item_type}[{index}]")

    total = len(occurrences)
    valid_occurrences = sum(
        1 for citation in occurrences if citation in transcript_codes
    )
    validity_rate = valid_occurrences / total if total > 0 else 0.0

    return {
        'valid': (
            total > 0
            and not invalid_codes
            and not missing_citation_items
            and not unclear_only_items
        ),
        'total_citations': total,
        'unique_citations': len(output_codes),
        'valid_citations': valid_codes,
        'invalid_citations': invalid_codes,
        'unclear_citations': unclear_codes,
        'missing_citation_items': missing_citation_items,
        'unclear_only_items': unclear_only_items,
        'validity_rate': validity_rate,
    }


def filter_invalid_items(
    output: dict,
    transcript: ParsedTranscript,
) -> Tuple[dict, List[dict]]:
    """Remove items with invalid citations from Study Pack output.

    Per PROJECT_RULES and spec §5 (kịch bản #1): items without valid
    citations must not be shown to the user.

    Args:
        output: Parsed JSON output from LLM.
        transcript: Parsed transcript used as source.

    Returns:
        Tuple of (filtered_output, removed_items).
        - filtered_output: Same structure with invalid items removed.
        - removed_items: List of items that were removed, with reason.
    """
    transcript_codes = transcript.get_lecture_citation_codes()
    removed = []

    def citation_issue(citations: object) -> Tuple[str, List[str]]:
        if not isinstance(citations, list) or not citations:
            return "Item không có citation.", []
        if not all(isinstance(citation, str) for citation in citations):
            return "Citation phải là danh sách mã đoạn dạng chuỗi.", []

        invalid = [citation for citation in citations if citation not in transcript_codes]
        if invalid:
            return f"Citation không tồn tại trong transcript: {invalid}", invalid

        clear_citations = [
            citation for citation in citations
            if not transcript.get_segment(citation).has_unclear
        ]
        if not clear_citations:
            return "Item chỉ dựa trên đoạn có [không nghe rõ].", []
        return "", []

    # Filter key_points
    filtered_key_points = []
    for kp in output.get('key_points', []):
        cites = kp.get('citations', [])
        reason, invalid = citation_issue(cites)
        if not reason:
            filtered_key_points.append(kp)
        else:
            removed.append({
                'type': 'key_point',
                'content': kp.get('content', ''),
                'reason': reason,
                'invalid_citations': invalid,
            })

    # Filter questions
    filtered_questions = []
    for q in output.get('questions', []):
        cites = q.get('citations', [])
        reason, invalid = citation_issue(cites)
        if not reason:
            filtered_questions.append(q)
        else:
            removed.append({
                'type': 'question',
                'content': q.get('question', ''),
                'reason': reason,
                'invalid_citations': invalid,
            })

    source_text = '\n'.join(
        segment.text for segment in transcript.get_lecture_segments()
    ).casefold()
    filtered_keywords = []
    for keyword in output.get('keywords', []):
        keyword_pattern = (
            re.escape(keyword.strip().casefold())
            if isinstance(keyword, str)
            else ''
        )
        if keyword_pattern and re.search(
            rf'(?<!\w){keyword_pattern}(?!\w)', source_text
        ):
            filtered_keywords.append(keyword)
        else:
            removed.append({
                'type': 'keyword',
                'content': keyword if isinstance(keyword, str) else repr(keyword),
                'reason': 'Keyword không xuất hiện trong transcript đã gửi model.',
                'invalid_citations': [],
            })

    filtered_output = {
        **output,
        'key_points': filtered_key_points,
        'keywords': filtered_keywords,
        'questions': filtered_questions,
    }

    return filtered_output, removed


def generate_validation_report(
    output: dict,
    transcript: ParsedTranscript,
) -> str:
    """Generate a human-readable validation report.

    Args:
        output: Parsed JSON output from LLM.
        transcript: Parsed transcript used as source.

    Returns:
        Formatted report string.
    """
    result = validate_citations(output, transcript)
    lines = [
        f"=== Citation Validation Report ===",
        f"Transcript: {transcript.title} (T{transcript.transcript_id})",
        f"Total citations in output: {result['total_citations']}",
        f"Unique citation codes: {result['unique_citations']}",
        f"Valid: {len(result['valid_citations'])}",
        f"Invalid: {len(result['invalid_citations'])}",
        f"Unclear source: {len(result['unclear_citations'])}",
        f"Validity rate: {result['validity_rate']:.1%}",
        f"Overall: {'✓ PASS' if result['valid'] else '✗ FAIL'}",
    ]

    if result['invalid_citations']:
        lines.append(f"\nInvalid citation codes:")
        for code in result['invalid_citations']:
            lines.append(f"  ✗ [{code}] — not found in transcript")

    if result['missing_citation_items']:
        lines.append("\nItems without citations:")
        for item_path in result['missing_citation_items']:
            lines.append(f"  ✗ {item_path}")

    if result['unclear_only_items']:
        lines.append("\nItems relying only on unclear source:")
        for item_path in result['unclear_only_items']:
            lines.append(f"  ✗ {item_path}")

    if result['unclear_citations']:
        lines.append(f"\nCitations pointing to unclear source:")
        for code in result['unclear_citations']:
            lines.append(f"  ⚠ [{code}] — contains [không nghe rõ]")

    return '\n'.join(lines)


# --- CLI usage for testing ---
if __name__ == '__main__':
    import json
    import sys

    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

    if len(sys.argv) < 3:
        print("Usage: python citation_validator.py <transcript.md> <output.json>")
        sys.exit(1)

    from transcript_parser import parse_transcript

    transcript = parse_transcript(sys.argv[1])
    with open(sys.argv[2], 'r', encoding='utf-8') as f:
        output = json.load(f)

    if 'study_pack' in output:
        output = output['study_pack']

    report = generate_validation_report(output, transcript)
    print(report)
