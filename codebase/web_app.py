"""Local clickable Study Pack flow backed by the real generator."""

import argparse
import json
import sys
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from study_pack_generator import (
    MissingAPIKeyError,
    UnsupportedObjectiveError,
    generate_study_pack,
)
from transcript_parser import parse_transcript


REPO_ROOT = Path(__file__).resolve().parents[1]
WEB_ROOT = Path(__file__).resolve().parent / 'web'
TRANSCRIPT_ROOT = REPO_ROOT / 'data' / 'study-pack-corpus' / 'transcript'
TRACE_ROOT = REPO_ROOT / 'codebase' / 'traces'
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
        if parsed_url.path == '/api/transcripts':
            self._list_transcripts()
            return
        if parsed_url.path == '/api/citation':
            self._get_citation(parse_qs(parsed_url.query))
            return
        self._serve_static(parsed_url.path)

    def do_POST(self) -> None:
        if urlparse(self.path).path != '/api/generate':
            self._send_json(HTTPStatus.NOT_FOUND, {'error': 'Not found.'})
            return

        content_type = self.headers.get_content_type()
        if content_type != 'application/json':
            self._send_json(
                HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                {
                    'status': 'invalid_request',
                    'message': 'Content-Type must be application/json.',
                },
            )
            return

        try:
            content_length = int(self.headers.get('Content-Length', '0'))
            if content_length <= 0 or content_length > 10_000:
                raise ValueError('Request body must be between 1 and 10000 bytes.')
            payload = json.loads(self.rfile.read(content_length))
            if not isinstance(payload, dict):
                raise ValueError('Request body must be a JSON object.')
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(
                HTTPStatus.BAD_REQUEST,
                {'status': 'invalid_request', 'message': str(error)},
            )
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

        self._send_json(
            HTTPStatus.OK,
            {
                'status': metadata['status'],
                'study_pack': study_pack,
                'metadata': {
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
            },
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

    def _send_json(self, status: HTTPStatus, payload: dict) -> None:
        content = json.dumps(payload, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description='Run the local Study Pack web app.')
    parser.add_argument('--port', default=8000, type=int)
    args = parser.parse_args()

    host = '0.0.0.0'
    server = ThreadingHTTPServer((host, args.port), StudyPackHandler)
    print(f'Study Pack running at http://{host}:{args.port}')
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
