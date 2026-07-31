const form = document.querySelector('#generate-form');
const transcriptSelect = document.querySelector('#transcript-select');
const statusPanel = document.querySelector('#status-panel');
const result = document.querySelector('#result');
const warnings = document.querySelector('#warnings');
const keyPoints = document.querySelector('#key-points');
const keywords = document.querySelector('#keywords');
const questions = document.querySelector('#questions');
const regenerate = document.querySelector('#regenerate');
const dialog = document.querySelector('#citation-dialog');
const questionTemplate = document.querySelector('#question-template');
const transcriptMeta = document.querySelector('#transcript-meta');
const resultContext = document.querySelector('#result-context');
const submitButton = form.querySelector('button[type="submit"]');
const submitLabel = submitButton.querySelector('.button-label');
let activeTranscript = '';
let transcriptCatalog = [];

function displayTitle(title) {
  return title
    .replace('Study Pack corpus - ', '')
    .replace('Transcript bài giảng (bản sạch) — ', '');
}

function updateTranscriptMeta() {
  const selected = transcriptCatalog.find((item) => item.file_name === transcriptSelect.value);
  if (!selected) {
    transcriptMeta.textContent = 'Chọn một nguồn để xem thông tin transcript.';
    return;
  }

  transcriptMeta.innerHTML = '';
  const id = document.createElement('strong');
  id.textContent = selected.transcript_id;
  const detail = document.createTextNode(
    ` · ${selected.segments.toLocaleString('vi-VN')} đoạn nguồn`
    + (selected.unclear_markers
      ? ` · ${selected.unclear_markers} đoạn cần kiểm tra`
      : ' · Không có marker [không nghe rõ]'),
  );
  transcriptMeta.append(id, detail);
}

function setStatus(kind, title, detail = '') {
  statusPanel.hidden = false;
  statusPanel.className = `status-panel ${kind}`;
  statusPanel.innerHTML = '';
  const heading = document.createElement('strong');
  heading.textContent = title;
  statusPanel.append(heading);
  if (detail) {
    const paragraph = document.createElement('p');
    paragraph.textContent = detail;
    statusPanel.append(paragraph);
  }
}

function citationButton(code) {
  const button = document.createElement('button');
  button.className = 'citation-button';
  button.type = 'button';
  button.textContent = `[${code}]`;
  button.addEventListener('click', () => openCitation(code));
  return button;
}

async function openCitation(code) {
  try {
    const params = new URLSearchParams({ transcript: activeTranscript, code });
    const response = await fetch(`/api/citation?${params}`);
    const payload = await response.json();
    if (!response.ok) {
      setStatus('error', 'Không mở được citation', payload.error || 'Không tìm thấy đoạn nguồn.');
      return;
    }
    document.querySelector('#citation-code').textContent = `[${payload.code}]`;
    document.querySelector('#citation-text').textContent = payload.text;
    document.querySelector('#citation-warning').hidden = !payload.has_unclear;
    dialog.showModal();
  } catch (error) {
    setStatus('error', 'Không mở được citation', error.message);
  }
}

function renderPack(payload) {
  activeTranscript = payload.transcript.file_name;
  keyPoints.innerHTML = '';
  keywords.innerHTML = '';
  questions.innerHTML = '';
  resultContext.textContent = `${payload.transcript.transcript_id} · ${displayTitle(payload.transcript.title)}`;

  const pack = payload.study_pack;
  pack.key_points.forEach((item) => {
    const row = document.createElement('li');
    const content = document.createElement('p');
    content.textContent = item.content;
    const cites = document.createElement('div');
    cites.className = 'citation-list';
    item.citations.forEach((code) => cites.append(citationButton(code)));
    row.append(content, cites);
    keyPoints.append(row);
  });

  pack.keywords.forEach((keyword) => {
    const chip = document.createElement('span');
    chip.textContent = keyword;
    keywords.append(chip);
  });

  pack.questions.forEach((item, index) => {
    const fragment = questionTemplate.content.cloneNode(true);
    const card = fragment.querySelector('.question-card');
    fragment.querySelector('.question-number').textContent = String(index + 1).padStart(2, '0');
    fragment.querySelector('h4').textContent = item.question;
    const answer = fragment.querySelector('.answer');
    answer.querySelector('p').textContent = item.answer;
    const citeList = answer.querySelector('.citation-list');
    item.citations.forEach((code) => citeList.append(citationButton(code)));

    const reveal = fragment.querySelector('.reveal-button');
    reveal.addEventListener('click', () => {
      answer.hidden = !answer.hidden;
      reveal.textContent = answer.hidden ? 'Hiện đáp án' : 'Ẩn đáp án';
      reveal.setAttribute('aria-expanded', String(!answer.hidden));
    });

    const feedbackButton = fragment.querySelector('.feedback-button');
    const feedbackReasons = fragment.querySelector('.feedback-reasons');
    feedbackButton.addEventListener('click', () => {
      feedbackReasons.hidden = !feedbackReasons.hidden;
      feedbackButton.setAttribute('aria-expanded', String(!feedbackReasons.hidden));
    });
    feedbackReasons.querySelectorAll('button').forEach((button) => {
      button.addEventListener('click', () => {
        feedbackReasons.querySelectorAll('button').forEach((itemButton) => itemButton.classList.remove('selected'));
        button.classList.add('selected');
        card.dataset.feedback = button.textContent;
      });
    });
    questions.append(fragment);
  });

  const warningItems = payload.metadata.warnings || [];
  warnings.hidden = warningItems.length === 0;
  warnings.innerHTML = '';
  warningItems.forEach((warning) => {
    const paragraph = document.createElement('p');
    paragraph.textContent = warning;
    warnings.append(paragraph);
  });

  statusPanel.hidden = true;
  result.hidden = false;
  result.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function generatePack(event) {
  event.preventDefault();
  result.hidden = true;
  setStatus('loading', 'Đang đọc transcript và tạo câu hỏi...', 'Lời gọi này dùng model thật; thường mất vài giây.');
  submitButton.disabled = true;
  submitButton.setAttribute('aria-busy', 'true');
  submitLabel.textContent = 'Đang tạo Study Pack...';

  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transcript: transcriptSelect.value,
        objective: document.querySelector('#objective').value,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      setStatus('error', 'Chưa thể tạo Study Pack', payload.message || 'Backend trả về lỗi.');
      return;
    }
    if (!payload.study_pack || payload.status === 'abstain') {
      setStatus('limited', 'Không đủ căn cứ để hiện Study Pack', (payload.metadata.warnings || []).join(' '));
      return;
    }
    renderPack(payload);
  } catch (error) {
    setStatus('error', 'Không kết nối được backend', error.message);
  } finally {
    submitButton.disabled = false;
    submitButton.removeAttribute('aria-busy');
    submitLabel.textContent = 'Tạo Study Pack';
  }
}

async function loadTranscripts() {
  try {
    const response = await fetch('/api/transcripts');
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'Server không trả về danh sách transcript.');
    transcriptCatalog = payload.transcripts;
    transcriptSelect.innerHTML = '<option value="">Chọn một nguồn học</option>';
    transcriptCatalog.forEach((transcript) => {
      const option = document.createElement('option');
      option.value = transcript.file_name;
      option.textContent = `${transcript.transcript_id} · ${displayTitle(transcript.title)}`;
      transcriptSelect.append(option);
    });
    transcriptMeta.textContent = `${transcriptCatalog.length} nguồn học sẵn sàng. Chọn một nguồn để bắt đầu.`;
  } catch (error) {
    transcriptSelect.innerHTML = '<option value="">Không tải được transcript</option>';
    transcriptMeta.textContent = 'Không thể đọc danh sách nguồn từ server.';
    setStatus('error', 'Không tải được data pack', error.message);
  }
}

form.addEventListener('submit', generatePack);
transcriptSelect.addEventListener('change', updateTranscriptMeta);
regenerate.addEventListener('click', () => form.requestSubmit());
document.querySelector('#close-dialog').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', (event) => {
  if (event.target === dialog) dialog.close();
});

loadTranscripts();
