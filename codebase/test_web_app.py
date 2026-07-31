"""HTTP smoke tests using only real data-pack and golden-set inputs."""

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

import web_app
from review_store import create_review_draft
from transcript_parser import parse_transcript
from web_app import StudyPackHandler


@pytest.fixture
def server_url():
    server = ThreadingHTTPServer(('127.0.0.1', 0), StudyPackHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


@pytest.fixture
def protected_server_url():
    server = ThreadingHTTPServer(('127.0.0.1', 0), StudyPackHandler)
    server.access_token = 'test-access-token-24-characters'
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}'
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_home_and_real_transcript_list(server_url: str) -> None:
    with urlopen(f'{server_url}/', timeout=5) as response:
        assert response.status == 200
        page = response.read().decode('utf-8')
    assert 'Study Pack 10 phút' in page
    assert 'data-dashboard="learner"' in page
    assert 'data-dashboard="teacher"' in page

    with urlopen(f'{server_url}/recall_session.js', timeout=5) as response:
        assert response.status == 200
        assert response.headers.get_content_type() == 'application/javascript'
        assert b'after one other queued question' in response.read()

    with urlopen(f'{server_url}/api/transcripts', timeout=5) as response:
        payload = json.load(response)
    assert len(payload['transcripts']) == 6
    assert payload['transcripts'][0]['file_name'] == 'transcript-10-clean.md'


def test_real_citation_endpoint(server_url: str) -> None:
    url = (
        f'{server_url}/api/citation?'
        'transcript=transcript-10-clean.md&code=T10-001'
    )
    with urlopen(url, timeout=5) as response:
        payload = json.load(response)

    assert payload['code'] == 'T10-001'
    assert payload['text']


def test_out_of_scope_golden_input_is_rejected_without_model(server_url: str) -> None:
    body = json.dumps({
        'transcript': 'transcript-10-clean.md',
        'objective': 'Cho tôi đáp án quiz chính thức buổi hôm nay',
    }).encode('utf-8')
    request = Request(
        f'{server_url}/api/generate',
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    with pytest.raises(HTTPError) as error:
        urlopen(request, timeout=5)

    assert error.value.code == 422
    payload = json.loads(error.value.read().decode('utf-8'))
    assert payload['status'] == 'rejected'
    assert payload['reason_code'] == 'official_answer_request'


def test_generate_rejects_non_object_json(server_url: str) -> None:
    request = Request(
        f'{server_url}/api/generate',
        data=b'[]',
        headers={'Content-Type': 'application/json'},
        method='POST',
    )

    with pytest.raises(HTTPError) as error:
        urlopen(request, timeout=5)

    assert error.value.code == 400
    payload = json.loads(error.value.read().decode('utf-8'))
    assert payload['status'] == 'invalid_request'


def test_protected_server_requires_bearer_token_for_data_api(
    protected_server_url: str,
) -> None:
    with urlopen(f'{protected_server_url}/health', timeout=5) as response:
        assert response.status == 200

    with pytest.raises(HTTPError) as error:
        urlopen(f'{protected_server_url}/api/transcripts', timeout=5)
    assert error.value.code == 401

    request = Request(
        f'{protected_server_url}/api/transcripts',
        headers={
            'Authorization': 'Bearer test-access-token-24-characters',
        },
    )
    with urlopen(request, timeout=5) as response:
        payload = json.load(response)
    assert len(payload['transcripts']) == 6


def test_recall_evaluation_uses_reviewed_question(
    server_url: str,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    """The HTTP endpoint must not accept an answer key from the browser."""
    monkeypatch.setattr(web_app, 'REVIEW_ROOT', tmp_path / 'reviews')
    transcript_path = web_app.TRANSCRIPT_FILES['transcript-10-clean.md']
    transcript = parse_transcript(str(transcript_path))
    study_pack = {
        'key_points': [{
            'content': 'Agentic AI tập trung vào lập kế hoạch và thực thi hành động.',
            'citations': ['T10-004'],
        }],
        'keywords': ['Agentic AI'],
        'questions': [{
            'question': 'Agentic AI nhấn mạnh khả năng nào?',
            'answer': 'Lập kế hoạch và thực thi hành động độc lập.',
            'citations': ['T10-004'],
        }],
    }
    review = create_review_draft(
        review_dir=str(web_app.REVIEW_ROOT),
        transcript_name='transcript-10-clean.md',
        transcript=transcript,
        study_pack=study_pack,
        objective='Ôn quiz trong 10 phút',
        generation_trace_id='test_trace',
    )

    received = {}

    def fake_evaluator(**kwargs):
        received.update(kwargs)
        return {
            'match_score': 72,
            'passed': True,
            'threshold': 60,
            'feedback': 'Nêu đúng khả năng trọng tâm.',
            'evidence_citations': ['T10-004'],
        }, {'provider': 'gemini', 'model': 'test', 'threshold': 60}

    monkeypatch.setattr(web_app, 'evaluate_active_recall_answer', fake_evaluator)
    request = Request(
        f'{server_url}/api/recall/evaluate',
        data=json.dumps({
            'draft_id': review['draft_id'],
            'question_index': 0,
            'learner_answer': 'Nó tự lập kế hoạch rồi thực hiện hành động.',
            # Deliberately ignored: canonical answer must come from the draft.
            'answer': 'browser-supplied answer must not be trusted',
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urlopen(request, timeout=5) as response:
        payload = json.load(response)

    assert payload['status'] == 'ok'
    assert payload['evaluation']['passed'] is True
    assert payload['evaluation']['match_score'] == 72
    assert received['question'] == study_pack['questions'][0]
    assert received['learner_answer'].startswith('Nó tự lập kế hoạch')
