"""Local clickable Study Pack flow backed by the real generator."""

import argparse
import hmac
import json
import os
import sys
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from study_pack_generator import (
    MissingAPIKeyError,
    UnsupportedObjectiveError,
    evaluate_active_recall_answer,
    generate_study_pack,
    regenerate_active_recall_question,
)
from review_store import (
    ReviewConflictError,
    ReviewNotFoundError,
    ReviewValidationError,
    approve_review_draft,
    create_review_draft,
    get_review_draft,
    update_review_draft,
)
from transcript_parser import parse_transcript


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = Path(__file__).resolve().parent / 'web'
TRANSCRIPT_ROOT = Path(os.environ.get(
    'STUDY_PACK_DATA_ROOT',
    str(REPO_ROOT / 'data' / 'study-pack-corpus' / 'transcript'),
)).resolve()
TRACE_ROOT = REPO_ROOT / 'codebase' / 'traces'
REVIEW_ROOT = TRACE_ROOT / 'reviews'
TRANSCRIPT_FILES = {
    path.name: path
    for path in sorted(TRANSCRIPT_ROOT.glob('transcript-??-clean.md'))
}
STATIC_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
}
GENERATION_SLOT = threading.BoundedSemaphore(value=1)


class StudyPackHandler(BaseHTTPRequestHandler):
    """Serve static assets and the narrow Study Pack JSON API."""

    server_version = 'StudyPack/1.0'

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/health':
            self._send_json(HTTPStatus.OK, {'status': 'ok'})
            return
        if (
            parsed_url.path.startswith('/api/')
            and not self._require_api_authorization()
        ):
            return
        if parsed_url.path == '/api/transcripts':
            self._list_transcripts()
            return
        if parsed_url.path == '/api/citation':
            self._get_citation(parse_qs(parsed_url.query))
            return
        if parsed_url.path == '/api/review':
            self._get_review(parse_qs(parsed_url.query))
            return
        self._serve_static(parsed_url.path)

    def do_POST(self) -> None:
        request_path = urlparse(self.path).path
        if (
            request_path.startswith('/api/')
            and not self._require_api_authorization()
        ):
            return
        if request_path == '/api/generate':
            self._generate()
            return
        if request_path == '/api/review/approve':
            self._approve_review()
            return
        if request_path == '/api/review/regenerate-question':
            self._regenerate_question()
            return
        if request_path == '/api/recall/evaluate':
            self._evaluate_recall_answer()
            return
        self._send_json(HTTPStatus.NOT_FOUND, {'error': 'Not found.'})

    def do_PATCH(self) -> None:
        request_path = urlparse(self.path).path
        if (
            request_path.startswith('/api/')
            and not self._require_api_authorization()
        ):
            return
        if request_path == '/api/review':
            self._update_review()
            return
        self._send_json(HTTPStatus.NOT_FOUND, {'error': 'Not found.'})

    def do_HEAD(self) -> None:
        request_path = urlparse(self.path).path
        if request_path not in {'/', '/health'}:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Length', '0')
        self.end_headers()

    def _require_api_authorization(self) -> bool:
        expected_token = getattr(self.server, 'access_token', None)
        if not expected_token:
            return True
        authorization = self.headers.get('Authorization', '')
        scheme, _, supplied_token = authorization.partition(' ')
        authorized = (
            scheme.casefold() == 'bearer'
            and bool(supplied_token)
            and hmac.compare_digest(supplied_token, expected_token)
        )
        if authorized:
            return True
        self._send_json(
            HTTPStatus.UNAUTHORIZED,
            {
                'status': 'access_required',
                'message': 'Cần mã truy cập hợp lệ để dùng dữ liệu khóa học.',
            },
            {'WWW-Authenticate': 'Bearer realm="Study Pack"'},
        )
        return False

    def _generate(self) -> None:
        payload = self._read_json_body(max_bytes=10_000)
        if payload is None:
            return

        transcript_name = payload.get('transcript')
        objective = payload.get('objective', 'Ôn quiz trong 10 phút')
        if not isinstance(transcript_name, str) or not isinstance(objective, str):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    'status': 'invalid_request',
                    'message': 'transcript and objective must be strings.',
                },
            )
            return
        transcript_path = TRANSCRIPT_FILES.get(transcript_name)
        if transcript_path is None:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {
                    'status': 'needs_input',
                    'message': 'Hãy chọn một transcript trong danh sách.',
                },
            )
            return

        if not GENERATION_SLOT.acquire(blocking=False):
            self._send_json(
                HTTPStatus.TOO_MANY_REQUESTS,
                {
                    'status': 'busy',
                    'message': 'Một lượt tạo khác đang chạy. Hãy thử lại sau.',
                },
            )
            return

        try:
            transcript = parse_transcript(str(transcript_path))
            study_pack, metadata = generate_study_pack(
                transcript=transcript,
                objective=objective,
                trace_dir=str(TRACE_ROOT),
            )
        except UnsupportedObjectiveError as error:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {
                    'status': 'rejected',
                    'reason_code': error.code,
                    'message': error.user_message,
                },
            )
            return
        except MissingAPIKeyError as error:
            self._send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {'status': 'configuration_error', 'message': str(error)},
            )
            return
        except ValueError as error:
            self._send_json(
                HTTPStatus.BAD_GATEWAY,
                {'status': 'model_output_error', 'message': str(error)},
            )
            return
        except Exception as error:
            self.log_error('Generation failed: %s', error)
            self._send_json(
                HTTPStatus.BAD_GATEWAY,
                {
                    'status': 'provider_error',
                    'message': 'Model provider failed. Check the server log and trace.',
                },
            )
            return
        finally:
            GENERATION_SLOT.release()

        review = None
        if study_pack is not None:
            review = create_review_draft(
                review_dir=str(REVIEW_ROOT),
                transcript_name=transcript_name,
                transcript=transcript,
                study_pack=study_pack,
                objective=objective,
                generation_trace_id=metadata['trace_id'],
            )
        self._send_json(
            HTTPStatus.OK,
            {
                'status': metadata['status'],
                'study_pack': study_pack,
                'metadata': {
                    'provider': metadata['provider'],
                    'model': metadata['model'],
                    'provider_attempts': metadata['provider_attempts'],
                    'fallback_used': metadata['fallback_used'],
                    'warnings': metadata['warnings'],
                    'trace_id': metadata['trace_id'],
                    'validation': metadata['validation'],
                    'removed_items': metadata['removed_items'],
                },
                'transcript': {
                    'file_name': transcript_name,
                    'title': transcript.title,
                    'transcript_id': f'T{transcript.transcript_id}',
                },
                'review': review,
            },
        )

    def _read_json_body(self, max_bytes: int = 100_000) -> dict | None:
        if self.headers.get_content_type() != 'application/json':
            self._send_json(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                {
                    'status': 'invalid_request',
                    'message': 'Content-Type must be application/json.',
                },
            )
            return None
        try:
            content_length = int(self.headers.get('Content-Length', '0'))
            if content_length <= 0 or content_length > max_bytes:
                raise ValueError(
                    f'Request body must be between 1 and {max_bytes} bytes.'
                )
            payload = json.loads(self.rfile.read(content_length))
            if not isinstance(payload, dict):
                raise ValueError('Request body must be a JSON object.')
            return payload
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {'status': 'invalid_request', 'message': str(error)},
            )
            return None

    def _review_context(self, draft_id: object) -> tuple[dict, object] | None:
        if not isinstance(draft_id, str):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {'status': 'invalid_request', 'message': 'draft_id is required.'},
            )
            return None
        try:
            review = get_review_draft(str(REVIEW_ROOT), draft_id)
        except ReviewNotFoundError as error:
            self._send_json(
                HTTPStatus.NOT_FOUND,
                {'status': 'not_found', 'message': str(error)},
            )
            return None
        transcript_path = TRANSCRIPT_FILES.get(
            review['transcript']['file_name']
        )
        if transcript_path is None:
            self._send_json(
                HTTPStatus.CONFLICT,
                {
                    'status': 'source_missing',
                    'message': 'Nguồn transcript của bản nháp không còn khả dụng.',
                },
            )
            return None
        return review, parse_transcript(str(transcript_path))

    def _get_review(self, query: dict) -> None:
        context = self._review_context(query.get('draft_id', [''])[0])
        if context is None:
            return
        review, _ = context
        self._send_json(HTTPStatus.OK, {'review': review})

    def _update_review(self) -> None:
        payload = self._read_json_body()
        if payload is None:
            return
        context = self._review_context(payload.get('draft_id'))
        if context is None:
            return
        review, transcript = context
        revision = payload.get('revision')
        study_pack = payload.get('study_pack')
        if not isinstance(revision, int) or not isinstance(study_pack, dict):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    'status': 'invalid_request',
                    'message': 'revision và study_pack là bắt buộc.',
                },
            )
            return
        try:
            updated = update_review_draft(
                review_dir=str(REVIEW_ROOT),
                draft_id=review['draft_id'],
                transcript=transcript,
                study_pack=study_pack,
                expected_revision=revision,
                action=payload.get('action', 'draft_saved'),
                details=payload.get('details'),
            )
        except ReviewConflictError as error:
            self._send_json(
                HTTPStatus.CONFLICT,
                {'status': 'conflict', 'message': str(error)},
            )
            return
        except ReviewValidationError as error:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {
                    'status': 'validation_error',
                    'message': str(error),
                    'validation': error.validation,
                },
            )
            return
        self._send_json(HTTPStatus.OK, {'status': 'saved', 'review': updated})

    def _approve_review(self) -> None:
        payload = self._read_json_body()
        if payload is None:
            return
        context = self._review_context(payload.get('draft_id'))
        if context is None:
            return
        review, transcript = context
        revision = payload.get('revision')
        study_pack = payload.get('study_pack')
        if not isinstance(revision, int) or not isinstance(study_pack, dict):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    'status': 'invalid_request',
                    'message': 'revision và study_pack là bắt buộc.',
                },
            )
            return
        try:
            approved = approve_review_draft(
                review_dir=str(REVIEW_ROOT),
                draft_id=review['draft_id'],
                transcript=transcript,
                study_pack=study_pack,
                expected_revision=revision,
            )
        except ReviewConflictError as error:
            self._send_json(
                HTTPStatus.CONFLICT,
                {'status': 'conflict', 'message': str(error)},
            )
            return
        except ReviewValidationError as error:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {
                    'status': 'validation_error',
                    'message': str(error),
                    'validation': error.validation,
                },
            )
            return
        self._send_json(
            HTTPStatus.OK,
            {'status': 'approved', 'review': approved},
        )

    def _regenerate_question(self) -> None:
        payload = self._read_json_body()
        if payload is None:
            return
        context = self._review_context(payload.get('draft_id'))
        if context is None:
            return
        review, transcript = context
        if review['status'] == 'approved':
            self._send_json(
                HTTPStatus.CONFLICT,
                {
                    'status': 'conflict',
                    'message': 'Study Pack đã duyệt nên không thể tạo lại câu.',
                },
            )
            return
        current_questions = payload.get('current_questions')
        if not isinstance(current_questions, list):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    'status': 'invalid_request',
                    'message': 'current_questions phải là danh sách.',
                },
            )
            return
        if not GENERATION_SLOT.acquire(blocking=False):
            self._send_json(
                HTTPStatus.TOO_MANY_REQUESTS,
                {
                    'status': 'busy',
                    'message': 'Model đang xử lý một lượt khác. Hãy thử lại sau.',
                },
            )
            return
        try:
            question, metadata = regenerate_active_recall_question(
                transcript=transcript,
                current_questions=current_questions,
                instruction=payload.get('instruction', ''),
                question_type=payload.get('question_type', 'explain'),
                difficulty=payload.get('difficulty', 'medium'),
                trace_dir=str(TRACE_ROOT),
            )
        except MissingAPIKeyError as error:
            self._send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {'status': 'configuration_error', 'message': str(error)},
            )
            return
        except ValueError as error:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {'status': 'model_output_error', 'message': str(error)},
            )
            return
        except Exception as error:
            self.log_error('Question regeneration failed: %s', error)
            self._send_json(
                HTTPStatus.BAD_GATEWAY,
                {
                    'status': 'provider_error',
                    'message': 'Model provider failed while regenerating question.',
                },
            )
            return
        finally:
            GENERATION_SLOT.release()
        self._send_json(
            HTTPStatus.OK,
            {'status': 'ok', 'question': question, 'metadata': metadata},
        )

    def _evaluate_recall_answer(self) -> None:
        """Evaluate one learner response only against the reviewed citations."""
        payload = self._read_json_body(max_bytes=5_000)
        if payload is None:
            return
        context = self._review_context(payload.get('draft_id'))
        if context is None:
            return
        review, transcript = context
        question_index = payload.get('question_index')
        learner_answer = payload.get('learner_answer')
        if (
            not isinstance(question_index, int)
            or isinstance(question_index, bool)
            or not isinstance(learner_answer, str)
        ):
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    'status': 'invalid_request',
                    'message': 'question_index và learner_answer là bắt buộc.',
                },
            )
            return
        questions = review['study_pack'].get('questions', [])
        if question_index < 0 or question_index >= len(questions):
            self._send_json(
                HTTPStatus.NOT_FOUND,
                {
                    'status': 'not_found',
                    'message': 'Không tìm thấy câu active recall cần đối chiếu.',
                },
            )
            return
        if not GENERATION_SLOT.acquire(blocking=False):
            self._send_json(
                HTTPStatus.TOO_MANY_REQUESTS,
                {
                    'status': 'busy',
                    'message': 'Model đang xử lý một lượt khác. Hãy thử lại sau.',
                },
            )
            return
        try:
            evaluation, metadata = evaluate_active_recall_answer(
                transcript=transcript,
                question=questions[question_index],
                learner_answer=learner_answer,
                trace_dir=str(TRACE_ROOT),
            )
        except MissingAPIKeyError as error:
            self._send_json(
                HTTPStatus.SERVICE_UNAVAILABLE,
                {'status': 'configuration_error', 'message': str(error)},
            )
            return
        except ValueError as error:
            self._send_json(
                HTTPStatus.UNPROCESSABLE_ENTITY,
                {'status': 'evaluation_error', 'message': str(error)},
            )
            return
        except Exception as error:
            self.log_error('Recall evaluation failed: %s', error)
            self._send_json(
                HTTPStatus.BAD_GATEWAY,
                {
                    'status': 'provider_error',
                    'message': 'Model provider failed while evaluating the answer.',
                },
            )
            return
        finally:
            GENERATION_SLOT.release()
        self._send_json(
            HTTPStatus.OK,
            {'status': 'ok', 'evaluation': evaluation, 'metadata': metadata},
        )

    def _list_transcripts(self) -> None:
        transcripts = []
        for file_name, path in TRANSCRIPT_FILES.items():
            transcript = parse_transcript(str(path))
            transcripts.append({
                'file_name': file_name,
                'transcript_id': f'T{transcript.transcript_id}',
                'title': transcript.title,
                'segments': transcript.total_segments,
                'unclear_markers': transcript.unclear_marker_count,
            })
        self._send_json(HTTPStatus.OK, {'transcripts': transcripts})

    def _get_citation(self, query: dict) -> None:
        transcript_name = query.get('transcript', [''])[0]
        citation_code = query.get('code', [''])[0]
        transcript_path = TRANSCRIPT_FILES.get(transcript_name)
        if transcript_path is None:
            self._send_json(HTTPStatus.NOT_FOUND, {'error': 'Transcript not found.'})
            return

        transcript = parse_transcript(str(transcript_path))
        segment = transcript.get_segment(citation_code)
        if segment is None or segment.is_activity:
            self._send_json(HTTPStatus.NOT_FOUND, {'error': 'Citation not found.'})
            return

        self._send_json(
            HTTPStatus.OK,
            {
                'code': segment.code,
                'text': segment.text,
                'has_unclear': segment.has_unclear,
                'line_number': segment.line_number,
            },
        )

    def _serve_static(self, request_path: str) -> None:
        relative_path = 'index.html' if request_path == '/' else request_path.lstrip('/')
        file_path = (WEB_ROOT / relative_path).resolve()
        try:
            file_path.relative_to(WEB_ROOT.resolve())
        except ValueError:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if not file_path.is_file() or file_path.suffix not in STATIC_TYPES:
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-Type', STATIC_TYPES[file_path.suffix])
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(
        self,
        status: HTTPStatus,
        payload: dict,
        extra_headers: dict | None = None,
    ) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        for name, value in (extra_headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description='Run the local Study Pack web app.')
    parser.add_argument(
        '--host',
        default=os.environ.get('HOST', '127.0.0.1'),
        help='Bind host; public binds require APP_ACCESS_TOKEN.',
    )
    parser.add_argument('--port', default=8000, type=int)
    args = parser.parse_args()

    public_bind = args.host not in {'127.0.0.1', 'localhost', '::1'}
    access_token = os.environ.get('APP_ACCESS_TOKEN', '').strip()
    if public_bind and len(access_token) < 24:
        raise SystemExit(
            'APP_ACCESS_TOKEN có ít nhất 24 ký tự là bắt buộc khi bind '
            'ra ngoài loopback.'
        )
    if not TRANSCRIPT_FILES:
        raise SystemExit(
            f'Không tìm thấy authorized transcript tại {TRANSCRIPT_ROOT}. '
            'Không dùng data thay thế.'
        )

    server = ThreadingHTTPServer((args.host, args.port), StudyPackHandler)
    server.access_token = access_token or None
    print(f'Study Pack running at http://{args.host}:{args.port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    main()
