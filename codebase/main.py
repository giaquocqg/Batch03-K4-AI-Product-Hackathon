"""
Main entry point for Study Pack generation.

Usage:
    python codebase/main.py --transcript data/vlearn-pack/transcript/transcript-01-clean.md
"""

import argparse
import json
import sys
from pathlib import Path

# Add codebase to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from transcript_parser import parse_transcript
from study_pack_generator import (
    MissingAPIKeyError,
    UnsupportedObjectiveError,
    generate_study_pack,
)
from citation_validator import generate_validation_report


def _save_output(output_path: str, study_pack: object, metadata: dict) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {'study_pack': study_pack, 'metadata': metadata},
            indent=2,
            ensure_ascii=False,
        ),
        encoding='utf-8',
    )


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    parser = argparse.ArgumentParser(
        description='Study Pack 10 phút — Tạo Study Pack từ transcript bài giảng'
    )
    parser.add_argument(
        '--transcript',
        required=False,
        help='Đường dẫn đến file transcript (ví dụ: data/vlearn-pack/transcript/transcript-01-clean.md)'
    )
    parser.add_argument(
        '--objective',
        default='Ôn quiz trong 10 phút',
        help='Mục tiêu ôn tập (mặc định: "Ôn quiz trong 10 phút")'
    )
    parser.add_argument(
        '--output',
        default=None,
        help='File JSON đầu ra (mặc định: in ra stdout)'
    )
    parser.add_argument(
        '--trace-dir',
        default='codebase/traces',
        help='Thư mục lưu trace (mặc định: codebase/traces)'
    )

    args = parser.parse_args()

    if not args.transcript:
        message = (
            'Cần chọn transcript trước khi tạo Study Pack. '
            'Dùng --transcript <path-to-transcript.md>.'
        )
        print(message, file=sys.stderr)
        if args.output:
            _save_output(
                args.output,
                None,
                {'status': 'needs_input', 'message': message},
            )
        return 2

    # Step 1: Parse transcript
    print(f"📄 Parsing transcript: {args.transcript}")
    transcript = parse_transcript(args.transcript)
    print(f"   Title: {transcript.title}")
    print(f"   Segments: {transcript.total_segments} "
          f"(lecture: {transcript.total_segments - transcript.activity_count}, "
          f"activity: {transcript.activity_count})")
    print(f"   Unclear segments: {transcript.unclear_count}")
    print(f"   Unclear markers: {transcript.unclear_marker_count}")
    print()

    # Step 2: Generate Study Pack via real LLM call
    print(f"🤖 Generating Study Pack...")
    print(f"   Objective: {args.objective}")
    try:
        study_pack, metadata = generate_study_pack(
            transcript=transcript,
            objective=args.objective,
            trace_dir=args.trace_dir,
        )
    except UnsupportedObjectiveError as error:
        print(f"Không thể tạo Study Pack: {error.user_message}", file=sys.stderr)
        if args.output:
            _save_output(
                args.output,
                None,
                {
                    'status': 'rejected',
                    'reason_code': error.code,
                    'message': error.user_message,
                    'transcript_id': f"T{transcript.transcript_id}",
                    'transcript_title': transcript.title,
                    'objective': args.objective,
                },
            )
        return 2
    except MissingAPIKeyError as error:
        print(f"Không thể gọi model: {error}", file=sys.stderr)
        if args.output:
            _save_output(
                args.output,
                None,
                {
                    'status': 'configuration_error',
                    'message': str(error),
                    'transcript_id': f"T{transcript.transcript_id}",
                    'transcript_title': transcript.title,
                    'objective': args.objective,
                },
            )
        return 2
    except ValueError as error:
        print(f"Model trả output không hợp lệ: {error}", file=sys.stderr)
        if args.output:
            _save_output(
                args.output,
                None,
                {
                    'status': 'model_output_error',
                    'message': str(error),
                    'transcript_id': f"T{transcript.transcript_id}",
                    'transcript_title': transcript.title,
                    'objective': args.objective,
                },
            )
        return 2
    except Exception as error:
        print(f"Model provider lỗi: {error}", file=sys.stderr)
        if args.output:
            _save_output(
                args.output,
                None,
                {
                    'status': 'provider_error',
                    'message': str(error),
                    'transcript_id': f"T{transcript.transcript_id}",
                    'transcript_title': transcript.title,
                    'objective': args.objective,
                },
            )
        return 2

    # Step 3: Print validation report
    if study_pack is not None:
        print()
        print(generate_validation_report(study_pack, transcript))
        print()

    # Step 4: Print warnings
    if metadata['warnings']:
        print("⚠️  Warnings:")
        for w in metadata['warnings']:
            print(f"   - {w}")
        print()

    # Step 5: Print removed items
    if metadata['removed_items']:
        print(f"🗑️  Removed {len(metadata['removed_items'])} items:")
        for item in metadata['removed_items']:
            print(f"   - [{item['type']}] {item['content'][:80]}...")
            print(f"     Reason: {item['reason']}")
        print()

    # Step 6: Display Study Pack
    if metadata['status'] == 'abstain' or study_pack is None:
        print("Không hiển thị Study Pack vì không còn đủ item có căn cứ.")
        print(f"Trace saved: {metadata['trace_path']}")
    else:
        print("=" * 60)
        print(f"📚 STUDY PACK — {transcript.title}")
        print(f"   Mục tiêu: {args.objective}")
        print("=" * 60)

        kps = study_pack.get('key_points', [])
        print(f"\n📌 Ý trọng tâm ({len(kps)}):")
        for i, kp in enumerate(kps, 1):
            cites = ', '.join(f'[{c}]' for c in kp.get('citations', []))
            print(f"   {i}. {kp['content']}")
            print(f"      Dựa trên: {cites}")

        kws = study_pack.get('keywords', [])
        print(f"\n🔑 Keywords ({len(kws)}): {', '.join(kws)}")

        qs = study_pack.get('questions', [])
        print(f"\n❓ Câu hỏi Active Recall ({len(qs)}):")
        for i, q in enumerate(qs, 1):
            cites = ', '.join(f'[{c}]' for c in q.get('citations', []))
            print(f"   {i}. {q['question']}")
            print(f"      [Đáp án ẩn; xem trường answer trong JSON output]")
            print(f"      Dựa trên: {cites}")

        print()
        print(f"📝 Trace saved: {metadata['trace_path']}")

    # Step 7: Save to file if requested
    if args.output:
        _save_output(
            args.output,
            study_pack,
            {
                'transcript_id': f"T{transcript.transcript_id}",
                'transcript_title': transcript.title,
                'objective': args.objective,
                'provider': metadata['provider'],
                'trace_id': metadata['trace_id'],
                'status': metadata['status'],
                'validation': metadata['validation'],
                'warnings': metadata['warnings'],
            },
        )
        print(f"💾 Output saved: {args.output}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
