"""
Golden Set Evaluator — Runs all 22 cases from golden_set.json.

Usage:
    python eval/run_golden_set.py [--provider openai|gemini] [--dry-run]
"""

import json
import sys
import os
import argparse
import codecs
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'codebase'))

from main import main as run_single_case


TRANSCRIPT_DIR = Path(__file__).parent.parent / 'data' / 'vlearn-pack' / 'transcript'
GOLDEN_SET = Path(__file__).parent / 'golden_set.json'
RESULTS_DIR = Path(__file__).parent / 'results'


def load_golden_set():
    with open(GOLDEN_SET, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_transcript_path(transcript_id):
    if transcript_id is None:
        return None
    return str(TRANSCRIPT_DIR / f"{transcript_id}.md")


def run_case(case, run_id, dry_run=False):
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

    if transcript_path is None:
        result['status'] = 'no_transcript'
        result['output'] = None
        result['note'] = 'Case yêu cầu không có transcript - cần test thủ công qua web/CLI'
        return result

    if dry_run:
        result['status'] = 'dry_run'
        result['output'] = None
        return result

    # Run the actual case
    output_file = RESULTS_DIR / run_id / f"{case_id}.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)

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
        else:
            result['output'] = None
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

    return result


def main():
    parser = argparse.ArgumentParser(description='Run golden set evaluation')
    parser.add_argument('--provider', default='openai', choices=['openai', 'gemini'])
    parser.add_argument('--dry-run', action='store_true', help='Print cases without running')
    parser.add_argument('--cases', nargs='*', help='Specific case IDs to run (e.g. GS-01 GS-02)')
    args = parser.parse_args()

    # Set provider env
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
    print(f"Provider: {args.provider}")
    print(f"Cases to run: {len(cases)}")
    print()

    all_results = []
    for i, case in enumerate(cases, 1):
        print(f"[{i}/{len(cases)}] Running {case['case_id']} ({case['category']})...")
        result = run_case(case, run_id, dry_run=args.dry_run)
        all_results.append(result)

        status = result.get('status', 'ok')
        if status == 'ok':
            output = result.get('output', {})
            if output and isinstance(output, dict):
                sp = output.get('study_pack', {})
                validation = output.get('metadata', {}).get('validation', {})
                print(f"  ✅ Status: {status}, Schema: {validation.get('schema_valid', 'N/A')}")
            else:
                print(f"  ✅ Status: {status}")
        else:
            print(f"  ⚠️  Status: {status} - {result.get('note', result.get('error', ''))}")
        print()

    # Save summary
    summary_path = RESULTS_DIR / run_id / 'summary.json'
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'run_id': run_id,
            'provider': args.provider,
            'timestamp': datetime.now().isoformat(),
            'total_cases': len(cases),
            'results': all_results,
        }, f, indent=2, ensure_ascii=False)

    print(f"=== Summary ===")
    print(f"Results saved: {summary_path}")

    # Quick stats
    ok_count = sum(1 for r in all_results if r.get('status') in (None, 'ok'))
    error_count = sum(1 for r in all_results if r.get('status') in ('error', 'provider_error'))
    skip_count = sum(1 for r in all_results if r.get('status') in ('no_transcript', 'dry_run'))
    print(f"OK: {ok_count}, Errors: {error_count}, Skipped: {skip_count}")


if __name__ == '__main__':
    main()
