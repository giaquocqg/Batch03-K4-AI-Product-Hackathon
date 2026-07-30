"""Build the active Study Pack corpus from one combined UTF-8 text export.

The transformation is deliberately mechanical:
- split only at the six explicit source markers;
- turn every non-empty source line into exactly one citation segment;
- preserve the normalized line text without summarizing or paraphrasing;
- record hashes and counts in a manifest for later integrity checks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


CORPUS_VERSION = "study-pack-corpus-v1"


@dataclass(frozen=True)
class SourceDefinition:
    transcript_number: str
    source_key: str
    marker: str
    title: str

    @property
    def citation_prefix(self) -> str:
        return f"T{self.transcript_number}"

    @property
    def file_name(self) -> str:
        return f"transcript-{self.transcript_number}-clean.md"


SOURCES = (
    SourceDefinition("10", "paper", "[Paper]", "Paper - AI & LLM Foundation"),
    SourceDefinition("11", "day-01", "[Day-01]", "Day 01 - AI & LLM Foundation"),
    SourceDefinition(
        "12",
        "day-02",
        "[Day-02]",
        "Day 02 - Từ yêu cầu mơ hồ đến Problem Statement",
    ),
    SourceDefinition("13", "day-03", "[Day-03]", "Day 03 - Agentic AI và ReAct"),
    SourceDefinition(
        "14",
        "day-04",
        "[Day-04]",
        "Day 04 - Prompt Engineering và Tool Calling",
    ),
    SourceDefinition(
        "15",
        "day-05",
        "[Day-05]",
        "Day 05 - AI Product Thinking và Requirements",
    ),
)


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_text(content: str) -> str:
    return sha256_bytes(content.encode("utf-8"))


def normalized_content_lines(lines: list[str]) -> list[str]:
    """Match the parser's evidence normalization while retaining all text."""
    return [line.strip() for line in lines if line.strip()]


def locate_source_starts(lines: list[str]) -> list[int]:
    starts: list[int] = []
    for source in SOURCES:
        matches = [
            index
            for index, line in enumerate(lines)
            if line.startswith(source.marker)
        ]
        if len(matches) != 1:
            raise ValueError(
                f"Expected exactly one marker {source.marker!r}; found {len(matches)}."
            )
        starts.append(matches[0])

    if starts != sorted(starts):
        raise ValueError("Source markers are not in the required Paper, Day 01-05 order.")
    if starts[0] != 0:
        raise ValueError("Unexpected content exists before the [Paper] marker.")
    return starts


def render_transcript(
    source: SourceDefinition,
    content_lines: list[str],
    source_line_start: int,
    source_line_end: int,
    source_sha256: str,
) -> str:
    header = [
        f"# Study Pack corpus - {source.title}",
        "",
        f"> Corpus version: `{CORPUS_VERSION}`",
        f"> Combined source SHA-256: `{source_sha256}`",
        f"> Original source lines: {source_line_start}-{source_line_end}",
        "> Transformation: one non-empty source line equals one citation segment;",
        "> no source text is summarized, paraphrased, or silently truncated.",
        "",
    ]
    body: list[str] = []
    for index, line in enumerate(content_lines, start=1):
        if index > 999:
            raise ValueError(
                f"{source.source_key} has more than 999 segments; citation format "
                "Txx-NNN cannot represent the full source."
            )
        body.append(f"**[{source.citation_prefix}-{index:03d}]** {line}")
        body.append("")
    return "\n".join(header + body).rstrip() + "\n"


def build_corpus(source_path: Path, output_dir: Path) -> dict:
    source_bytes = source_path.read_bytes()
    source_sha256 = sha256_bytes(source_bytes)
    text = source_bytes.decode("utf-8-sig")
    lines = text.splitlines()
    starts = locate_source_starts(lines)

    output_dir.mkdir(parents=True, exist_ok=True)
    file_records = []
    total_segments = 0

    for index, source in enumerate(SOURCES):
        start = starts[index]
        end = starts[index + 1] if index + 1 < len(starts) else len(lines)
        raw_slice = lines[start:end]
        content_lines = normalized_content_lines(raw_slice)
        rendered = render_transcript(
            source=source,
            content_lines=content_lines,
            source_line_start=start + 1,
            source_line_end=end,
            source_sha256=source_sha256,
        )
        output_path = output_dir / source.file_name
        with output_path.open("w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered)

        normalized_text = "\n".join(content_lines)
        file_records.append(
            {
                "source_key": source.source_key,
                "title": source.title,
                "file_name": source.file_name,
                "transcript_id": source.citation_prefix,
                "source_line_start": start + 1,
                "source_line_end": end,
                "source_line_count": len(raw_slice),
                "segment_count": len(content_lines),
                "normalized_content_sha256": sha256_text(normalized_text),
                "generated_file_sha256": sha256_bytes(output_path.read_bytes()),
                "first_segment_text": content_lines[0],
                "last_segment_text": content_lines[-1],
            }
        )
        total_segments += len(content_lines)

    manifest = {
        "corpus_version": CORPUS_VERSION,
        "source_file_name": source_path.name,
        "source_sha256": source_sha256,
        "source_total_lines": len(lines),
        "source_non_empty_lines": total_segments,
        "transcript_count": len(file_records),
        "total_segments": total_segments,
        "preservation_rule": (
            "Every non-empty source line is preserved once, in order, as one "
            "citation segment after edge-whitespace normalization."
        ),
        "files": file_records,
    }
    manifest_path = output_dir.parent / "manifest.json"
    with manifest_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert the combined Paper + Day 01-05 text into transcripts."
    )
    parser.add_argument("source", type=Path, help="Combined UTF-8 text export.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/study-pack-corpus/transcript"),
        help="Directory for the six generated transcript files.",
    )
    args = parser.parse_args()

    manifest = build_corpus(args.source.resolve(), args.output_dir.resolve())
    print(
        f"Built {manifest['transcript_count']} transcripts with "
        f"{manifest['total_segments']} segments; source SHA-256 "
        f"{manifest['source_sha256']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
