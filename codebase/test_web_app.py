"""HTTP smoke tests using only real data-pack and golden-set inputs."""

import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

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


def test_home_and_real_transcript_list(server_url: str) -> None:
    with urlopen(f'{server_url}/', timeout=5) as response:
        assert response.status == 200
        assert 'Study Pack 10 phút' in response.read().decode('utf-8')

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
