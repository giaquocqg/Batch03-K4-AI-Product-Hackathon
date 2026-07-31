"""
Golden Set Evaluator — Runs all 22 cases from golden_set.json.

Usage:
    python eval/run_golden_set.py [--provider openai|gemini] [--dry-run]
"""

import json
import hashlib
import sys
import os
import argparse
import codecs
from datetime import datetime
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'codebase'))

from main import main as run_single_case


TRANSCRIPT_DIR = (
    Path(__file__).parent.parent
    / 'data'
    / 'study-pack-corpus'
    / 'transcript'
)
GOLDEN_SET = Path(__file__).parent / 'golden_set.json'
RESULTS_DIR = Path(__file__).parent / 'results'
PRIVATE_RESULTS_DIR = Path(__file__).parent / 'private-results'
TRACE_DIR = Path(__file__).parent.parent / 'codebase' / 'traces'
DEFAULT_OBJECTIVE = 'Ôn quiz trong 10 phút'


def load_golden_set():
    with open(GOLDEN_SET, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_transcript_path(transcript_id):
    if transcript_id is None:
        return None
    return str(TRANSCRIPT_DIR / f"{transcript_id}.md")


def sanitize_model_output(output):
    """Keep reproducible metrics while removing protected generated content."""
    if not isinstance(output, dict):
        return output
    study_pack = output.get('study_pack')
    metadata_value = output.get('metadata')
    metadata = metadata_value if isinstance(metadata_value, dict) else {}
    sanitized = {
        'artifact_type': 'sanitized_public_evaluation_summary',
        'content_redacted': study_pack is not None,
        'status': output.get('status') or metadata.get('status'),
        'transcript_id': metadata.get('transcript_id'),
        'objective': output.get('objective') or metadata.get('objective'),
        'provider': metadata.get('provider'),
        'model': metadata.get('model'),
        'trace_id': metadata.get('trace_id'),
    }
    if output.get('reason_code'):
        sanitized['reason_code'] = output['reason_code']
    if isinstance(study_pack, dict):
        canonical = json.dumps(
            study_pack,
            ensure_ascii=False,
            sort_keys=True,
            separators=(',', ':'),
        ).encode('utf-8')
        citations = sorted({
            citation
            for section in ('key_points', 'questions')
            for item in study_pack.get(section, [])
            for citation in item.get('citations', [])
            if isinstance(citation, str)
        })
        sanitized['study_pack_sha256'] = hashlib.sha256(canonical).hexdigest()
        sanitized['output_summary'] = {
            'key_point_count': len(study_pack.get('key_points', [])),
            'keyword_count': len(study_pack.get('keywords', [])),
            'question_count': len(study_pack.get('questions', [])),
            'citation_codes': citations,
        }
    validation = metadata.get('validation')
    if isinstance(validation, dict):
        sanitized['validation_summary'] = {
            'valid': validation.get('valid'),
            'total_citations': validation.get('total_citations'),
            'unique_citations': validation.get('unique_citations'),
            'invalid_citation_count': len(
                validation.get('invalid_citations', [])
            ),
            'missing_citation_item_count': len(
                validation.get('missing_citation_items', [])
            ),
            'validity_rate': validation.get('validity_rate'),
        }
    sanitized['warning_count'] = len(metadata.get('warnings', []))
    sanitized['removed_item_count'] = len(metadata.get('removed_items', []))
    return sanitized


def sanitize_case_result(result):
    public_result = {
        key: value
        for key, value in result.items()
        if key != 'output'
    }
    public_result['output'] = sanitize_model_output(result.get('output'))
    return public_result


def _hydrate_runtime_metadata(output):
    """Fill safe provider/model fields from the local private trace."""
    if not isinstance(output, dict):
        return
    metadata = output.get('metadata')
    if not isinstance(metadata, dict):
        return
    trace_id = metadata.get('trace_id')
    if not isinstance(trace_id, str) or not trace_id:
        return
    trace_path = TRACE_DIR / f'trace_{trace_id}.json'
    if not trace_path.exists():
        return
    try:
        trace = json.loads(trace_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError):
        return
    metadata.setdefault('provider', trace.get('provider'))
    metadata.setdefault('model', trace.get('model'))


def _call_local_api(base_url, case):
    payload = {
        'transcript': case.get('input', {}).get('transcript') or '',
        'objective': (
            case.get('input', {}).get('objective')
            or DEFAULT_OBJECTIVE
        ),
    }
    request = Request(
        f"{base_url.rstrip('/')}/api/generate",
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )
    try:
        with urlopen(request, timeout=180) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        body = error.read().decode('utf-8', errors='replace')
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {
                'status': 'http_error',
                'message': body or str(error),
            }
        return error.code, payload


def _expected_statuses(case):
    explicit = case.get('expected_statuses')
    if isinstance(explicit, list) and explicit:
        return explicit
    # `limited` is an accepted safe outcome when unsupported items were
    # removed but the final displayed Study Pack still passes every
    # deterministic schema/citation/content-count gate.
    return ['ok', 'limited']


def _automated_evaluation(case, result):
    """Score deterministic CP3 gates without pretending semantic review."""
    status = result.get('status')
    output = result.get('output')
    output = output if isinstance(output, dict) else {}
    study_pack = output.get('study_pack')
    metadata = output.get('metadata')
    metadata = metadata if isinstance(metadata, dict) else {}
    validation = metadata.get('validation')
    validation = validation if isinstance(validation, dict) else {}
    expected_statuses = _expected_statuses(case)

    checks = {
        'expected_status': status in expected_statuses,
    }
    if status in ('ok', 'limited'):
        study_pack = study_pack if isinstance(study_pack, dict) else {}
        key_points = study_pack.get('key_points', [])
        questions = study_pack.get('questions', [])
        keywords = study_pack.get('keywords', [])
        citations = [
            citation
            for section in (key_points, questions)
            for item in section
            if isinstance(item, dict)
            for citation in item.get('citations', [])
            if isinstance(citation, str)
        ]
        transcript_id = case.get('transcript_id')
        expected_prefix = None
        if isinstance(transcript_id, str):
            suffix = transcript_id.removeprefix('transcript-').split('-')[0]
            expected_prefix = f'T{suffix}-'
        checks.update({
            'study_pack_present': bool(study_pack),
            'five_key_points': len(key_points) == 5,
            'five_questions': len(questions) == 5,
            'keywords_present': bool(keywords),
            'validator_valid': validation.get('valid') is True,
            'no_invalid_citations': not validation.get(
                'invalid_citations', []
            ),
            'no_missing_citations': not validation.get(
                'missing_citation_items', []
            ),
            'citation_source_isolation': bool(citations) and (
                expected_prefix is None
                or all(code.startswith(expected_prefix) for code in citations)
            ),
        })

    manual_review_required = status in ('ok', 'limited')
    return {
        'expected_statuses': expected_statuses,
        'checks': checks,
        'automated_pass': all(checks.values()),
        'manual_semantic_review_required': manual_review_required,
        'manual_dimensions_pending': (
            ['groundedness', 'relevance', 'active_recall']
            if manual_review_required
            else []
        ),
    }


def run_case(case, run_id, dry_run=False, base_url=None):
    case_id = case['case_id']
    transcript_id = case.get('transcript_id')
    objective = case['input']['objective']
    transcript_path = get_transcript_path(transcript_id)

    result = {
        'case_id': case_id,
        'category': case['category'],
        'transcript_id': transcript_id,
        'objective': objective,
        'expected_behavior': case['expected_behavior'],
        'eval_note': case.get('eval_note'),
        'run_timestamp': datetime.now().isoformat(),
        'run_id': run_id,
    }

    if transcript_path is None and not base_url:
        result['status'] = 'no_transcript'
        result['output'] = None
        result['note'] = 'Case yêu cầu không có transcript - cần test thủ công qua web/CLI'
        return result

    if dry_run:
        result['status'] = 'dry_run'
        result['output'] = None
        return result

    output_file = PRIVATE_RESULTS_DIR / run_id / f"{case_id}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if base_url:
        try:
            http_status, output = _call_local_api(base_url, case)
            _hydrate_runtime_metadata(output)
            result['http_status'] = http_status
            result['output'] = output
            result['status'] = output.get('status', 'invalid_response')
            output_file.write_text(
                json.dumps(output, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )
        except Exception as error:
            result['status'] = 'error'
            result['error'] = f'{type(error).__name__}: {error}'
            result['output'] = None
        result['automated_evaluation'] = _automated_evaluation(case, result)
        return result

    # Run the actual case directly through the CLI.
    # Temporarily override sys.argv for main.py
    old_argv = sys.argv
    sys.argv = [
        'main.py',
        '--transcript', transcript_path,
        '--objective', objective,
        '--output', str(output_file),
    ]

    try:
        exit_code = run_single_case()
        result['exit_code'] = exit_code
        if output_file.exists():
            with open(output_file, 'r', encoding='utf-8') as f:
                result['output'] = json.load(f)
            metadata = result['output'].get('metadata', {})
            result['status'] = metadata.get('status', 'invalid_response')
        else:
            result['output'] = None
            result['status'] = 'error'
            result['note'] = f'Exit code {exit_code} but no output file'
    except SystemExit as e:
        result['exit_code'] = e.code
        result['output'] = None
        result['note'] = f'SystemExit: {e.code}'
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
        result['output'] = None
    finally:
        sys.argv = old_argv

    result['automated_evaluation'] = _automated_evaluation(case, result)
    return result


def main():
    parser = argparse.ArgumentParser(description='Run golden set evaluation')
    parser.add_argument('--provider', default='openai', choices=['openai', 'gemini'])
    parser.add_argument(
        '--base-url',
        help=(
            'Run through an already configured local web app, for example '
            'http://127.0.0.1:8000'
        ),
    )
    parser.add_argument('--dry-run', action='store_true', help='Print cases without running')
    parser.add_argument('--cases', nargs='*', help='Specific case IDs to run (e.g. GS-01 GS-02)')
    args = parser.parse_args()

    # Set provider env only for direct CLI execution. API mode deliberately
    # reuses the already configured server process without copying secrets.
    if not args.base_url:
        if args.provider == 'openai':
            os.environ['PROVIDER'] = 'openai'
        else:
            os.environ['PROVIDER'] = 'gemini'

    golden = load_golden_set()
    cases = golden['cases']

    if args.cases:
        cases = [c for c in cases if c['case_id'] in args.cases]

    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"=== Golden Set Evaluation ===")
    print(f"Run ID: {run_id}")
    print(
        f"Execution: {'local_api' if args.base_url else 'direct_cli'}"
    )
    print(f"Provider request: {args.provider if not args.base_url else 'runtime'}")
    print(f"Cases to run: {len(cases)}")
    print()

    all_results = []
    for i, case in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] Running {case['case_id']} ({case['category']})...")
        result = run_case(
            case,
            run_id,
            dry_run=args.dry_run,
            base_url=args.base_url,
        )
        all_results.append(result)
        public_case_path = RESULTS_DIR / run_id / f"{case['case_id']}.json"
        public_case_path.parent.mkdir(parents=True, exist_ok=True)
        with open(public_case_path, 'w', encoding='utf-8') as public_case_file:
            json.dump(
                sanitize_case_result(result),
                public_case_file,
                indent=2,
                ensure_ascii=False,
            )

        status = result.get('status', 'invalid_response')
        automated = result.get('automated_evaluation', {})
        if status == 'ok':
            output = result.get('output', {})
            if output and isinstance(output, dict):
                sp = output.get('study_pack', {})
                validation = output.get('metadata', {}).get('validation', {})
                print(
                    f"  ✅ Status: {status}, "
                    f"Validator: {validation.get('valid', 'N/A')}, "
                    f"Automated gate: {automated.get('automated_pass', False)}"
                )
            else:
                print(f"  ✅ Status: {status}")
        else:
            print(f"  ⚠️  Status: {status} - {result.get('note', result.get('error', ''))}")
        print()

    # Save summary
    summary_path = RESULTS_DIR / run_id / 'summary.json'
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        automated_pass_count = sum(
            1
            for result in all_results
            if result.get('automated_evaluation', {}).get('automated_pass')
        )
        manual_pending_count = sum(
            1
            for result in all_results
            if result.get('automated_evaluation', {}).get(
                'manual_semantic_review_required'
            )
        )
        automated_pass_rate = (
            automated_pass_count / len(all_results) * 100
            if all_results
            else 0
        )
        json.dump({
            'run_id': run_id,
            'execution_mode': (
                'local_api' if args.base_url else 'direct_cli'
            ),
            'provider_request': (
                'runtime' if args.base_url else args.provider
            ),
            'timestamp': datetime.now().isoformat(),
            'total_cases': len(cases),
            'automated_pass_count': automated_pass_count,
            'automated_pass_rate': round(automated_pass_rate, 2),
            'manual_semantic_review_pending_count': manual_pending_count,
            'final_quality_bar_pass': (
                None if manual_pending_count else automated_pass_rate >= 85
            ),
            'quality_bar_note': (
                'Không kết luận quality bar cuối cùng khi các chiều ngữ nghĩa '
                'còn chờ người chấm đọc output và citation nguồn.'
            ),
            'results': [
                sanitize_case_result(result)
                for result in all_results
            ],
        }, f, indent=2, ensure_ascii=False)

    print(f"=== Summary ===")
    print(f"Results saved: {summary_path}")

    # Quick stats
    ok_count = sum(1 for r in all_results if r.get('status') == 'ok')
    error_count = sum(1 for r in all_results if r.get('status') in ('error', 'provider_error'))
    skip_count = sum(1 for r in all_results if r.get('status') in ('no_transcript', 'dry_run'))
    print(f"OK: {ok_count}, Errors: {error_count}, Skipped: {skip_count}")
    print(
        f"Automated gate: {automated_pass_count}/{len(all_results)} "
        f"({automated_pass_rate:.2f}%)"
    )
    print(f"Manual semantic review pending: {manual_pending_count}")


if __name__ == '__main__':
    main()
