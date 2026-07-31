const form = document.querySelector('#generate-form');
const transcriptSelect = document.querySelector('#transcript-select');
const statusPanel = document.querySelector('#status-panel');
const result = document.querySelector('#result');
const warnings = document.querySelector('#warnings');
const keyPoints = document.querySelector('#key-points');
const keywords = document.querySelector('#keywords');
const questions = document.querySelector('#questions');
const regenerate = document.querySelector('#regenerate');
const citationDialog = document.querySelector('#citation-dialog');
const regenerateDialog = document.querySelector('#regenerate-dialog');
const questionTemplate = document.querySelector('#question-template');
const transcriptMeta = document.querySelector('#transcript-meta');
const resultContext = document.querySelector('#result-context');
const submitButton = form.querySelector('button[type="submit"]');
const submitLabel = submitButton.querySelector('.button-label');
const toggleEditButton = document.querySelector('#toggle-edit');
const saveReviewButton = document.querySelector('#save-review');
const approveReviewButton = document.querySelector('#approve-review');
const addQuestionButton = document.querySelector('#add-question');
const reviewStatus = document.querySelector('#review-status');
const reviewTitle = document.querySelector('#review-title');
const reviewProgress = document.querySelector('#review-progress');
const reviewMessage = document.querySelector('#review-message');
const reviewPanel = document.querySelector('#review-panel');
const dashboardNotice = document.querySelector('#dashboard-notice');
const dashboardButtons = document.querySelectorAll('.dashboard-switch button[data-dashboard]');
const accessGate = document.querySelector('#access-gate');
const accessForm = document.querySelector('#access-form');
const accessTokenInput = document.querySelector('#access-token');
const accessMessage = document.querySelector('#access-message');
const ACCESS_TOKEN_KEY = 'study-pack-access-token';

let activeTranscript = '';
let transcriptCatalog = [];
let currentPack = null;
let activeReview = null;
let editMode = false;
let hasUnsavedChanges = false;
let regenerationIndex = null;
let recallSession = null;
let dashboardMode = 'learner';

function displayTitle(title) {
  return title
    .replace('Study Pack corpus - ', '')
    .replace('Transcript bài giảng (bản sạch) — ', '');
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function setDashboard(mode, updateAddress = true) {
  dashboardMode = mode === 'teacher' ? 'teacher' : 'learner';
  document.body.dataset.dashboard = dashboardMode;
  dashboardButtons.forEach((button) => {
    const selected = button.dataset.dashboard === dashboardMode;
    button.classList.toggle('selected', selected);
    button.setAttribute('aria-pressed', String(selected));
  });
  dashboardNotice.textContent = dashboardMode === 'teacher'
    ? 'Dashboard giảng viên: kiểm tra, sửa, tạo lại và phê duyệt Study Pack trước khi phát hành. Đây là chế độ giao diện demo, chưa phải phân quyền bằng tài khoản.'
    : 'Dashboard học viên: chỉ hiện lượt active recall. Nhập đáp án trước khi đối chiếu nguồn.';
  if (dashboardMode === 'learner') editMode = false;
  if (updateAddress) {
    const url = new URL(window.location.href);
    if (dashboardMode === 'teacher') url.searchParams.set('dashboard', 'teacher');
    else url.searchParams.delete('dashboard');
    window.history.replaceState({}, '', url);
  }
  if (currentPack) {
    renderKeyPoints();
    renderKeywords();
    renderQuestions();
  }
  updateReviewUI();
}

async function apiFetch(url, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = sessionStorage.getItem(ACCESS_TOKEN_KEY);
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const response = await fetch(url, { ...options, headers });
  if (response.status === 401) {
    accessGate.hidden = false;
    accessTokenInput.focus();
  }
  return response;
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

function setReviewMessage(message, kind = '') {
  reviewMessage.textContent = message;
  reviewMessage.className = `review-message ${kind}`.trim();
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
    const response = await apiFetch(`/api/citation?${params}`);
    const payload = await response.json();
    if (!response.ok) {
      setStatus('error', 'Không mở được citation', payload.error || 'Không tìm thấy đoạn nguồn.');
      return;
    }
    document.querySelector('#citation-code').textContent = `[${payload.code}]`;
    document.querySelector('#citation-text').textContent = payload.text;
    document.querySelector('#citation-warning').hidden = !payload.has_unclear;
    citationDialog.showModal();
  } catch (error) {
    setStatus('error', 'Không mở được citation', error.message);
  }
}

function parseCitations(value) {
  return [...new Set(value.split(',').map((code) => code.trim()).filter(Boolean))];
}

function markDirty(message = 'Có thay đổi chưa lưu.') {
  if (!activeReview || activeReview.status === 'approved') return;
  hasUnsavedChanges = true;
  saveReviewButton.disabled = false;
  setReviewMessage(message, 'pending');
  updateReviewUI();
}

function updateReviewUI() {
  if (!activeReview || !currentPack) return;
  const approved = activeReview.status === 'approved';
  const teacherView = dashboardMode === 'teacher';
  const questionCount = currentPack.questions.length;
  const required = activeReview.required_questions;

  reviewStatus.textContent = approved ? 'Đã phê duyệt' : (hasUnsavedChanges ? 'Chưa lưu' : 'Bản nháp AI');
  reviewStatus.className = `review-status ${approved ? 'approved' : (hasUnsavedChanges ? 'pending' : 'draft')}`;
  reviewTitle.textContent = approved
    ? 'Study Pack đã được giảng viên phê duyệt'
    : 'Đây là bản nháp AI, chưa phát hành';
  reviewProgress.textContent = approved
    ? `${questionCount} câu · citation hợp lệ · bản đã khóa`
    : `${questionCount}/${required} câu cần có · revision ${activeReview.revision} · ${editMode ? 'đang kiểm duyệt nội dung' : 'có thể làm thử active recall như học viên'}`;

  reviewPanel.hidden = !teacherView;
  toggleEditButton.hidden = approved || !teacherView;
  saveReviewButton.hidden = approved || !teacherView;
  approveReviewButton.hidden = approved || !teacherView;
  toggleEditButton.textContent = editMode
    ? 'Quay lại lượt active recall'
    : 'Mở chế độ kiểm duyệt';
  saveReviewButton.disabled = !hasUnsavedChanges;
  addQuestionButton.hidden = !editMode || approved || questionCount >= 5;
}

function renderKeyPoints() {
  keyPoints.innerHTML = '';
  currentPack.key_points.forEach((item) => {
    const row = document.createElement('li');
    const content = document.createElement('p');
    content.textContent = item.content;
    const cites = document.createElement('div');
    cites.className = 'citation-list';
    item.citations.forEach((code) => cites.append(citationButton(code)));
    row.append(content, cites);
    keyPoints.append(row);
  });
}

function renderKeywords() {
  keywords.innerHTML = '';
  currentPack.keywords.forEach((keyword) => {
    const chip = document.createElement('span');
    chip.textContent = keyword;
    keywords.append(chip);
  });
}

function moveQuestion(index, offset) {
  const destination = index + offset;
  if (destination < 0 || destination >= currentPack.questions.length) return;
  const [item] = currentPack.questions.splice(index, 1);
  currentPack.questions.splice(destination, 0, item);
  markDirty('Đã đổi thứ tự câu hỏi. Hãy lưu bản nháp.');
  renderQuestions();
}

function deleteQuestion(index) {
  if (currentPack.questions.length <= 1) {
    setReviewMessage('Study Pack phải còn ít nhất một câu hỏi.', 'error');
    return;
  }
  currentPack.questions.splice(index, 1);
  markDirty('Đã xóa câu. Thêm câu thay thế trước khi phê duyệt.');
  renderQuestions();
}

function openRegeneration(index) {
  regenerationIndex = index;
  document.querySelector('#regenerate-instruction').value = '';
  regenerateDialog.showModal();
}

function renderQuestions() {
  const approved = activeReview && activeReview.status === 'approved';
  if (dashboardMode === 'teacher' && editMode && !approved) {
    renderReviewQuestions();
    return;
  }
  renderRecallSession();
}

function renderReviewQuestions() {
  questions.innerHTML = '';
  const approved = activeReview && activeReview.status === 'approved';

  currentPack.questions.forEach((item, index) => {
    const fragment = questionTemplate.content.cloneNode(true);
    const card = fragment.querySelector('.question-card');
    fragment.querySelector('.question-number').textContent = String(index + 1).padStart(2, '0');
    fragment.querySelector('h4').textContent = item.question || 'Câu hỏi mới chưa hoàn tất';
    const answer = fragment.querySelector('.answer');
    answer.querySelector('p').textContent = item.answer || 'Chưa có đáp án.';
    const citeList = answer.querySelector('.citation-list');
    item.citations.forEach((code) => citeList.append(citationButton(code)));

    const reveal = fragment.querySelector('.reveal-button');
    reveal.addEventListener('click', () => {
      answer.hidden = !answer.hidden;
      reveal.textContent = answer.hidden ? 'Hiện đáp án' : 'Ẩn đáp án';
      reveal.setAttribute('aria-expanded', String(!answer.hidden));
    });

    const actions = fragment.querySelector('.question-review-actions');
    const editor = fragment.querySelector('.question-editor');
    actions.hidden = !editMode || approved;
    editor.hidden = !editMode || approved;
    reveal.hidden = editMode && !approved;
    card.classList.toggle('editing', editMode && !approved);

    actions.querySelector('[data-action="move-up"]').disabled = index === 0;
    actions.querySelector('[data-action="move-down"]').disabled = index === currentPack.questions.length - 1;
    actions.querySelector('[data-action="move-up"]').addEventListener('click', () => moveQuestion(index, -1));
    actions.querySelector('[data-action="move-down"]').addEventListener('click', () => moveQuestion(index, 1));
    actions.querySelector('[data-action="delete"]').addEventListener('click', () => deleteQuestion(index));
    actions.querySelector('[data-action="regenerate"]').addEventListener('click', () => openRegeneration(index));

    const questionInput = editor.querySelector('.question-input');
    const answerInput = editor.querySelector('.answer-input');
    const citationsInput = editor.querySelector('.citations-input');
    questionInput.value = item.question;
    answerInput.value = item.answer;
    citationsInput.value = item.citations.join(', ');
    questionInput.addEventListener('input', () => {
      item.question = questionInput.value;
      markDirty();
    });
    answerInput.addEventListener('input', () => {
      item.answer = answerInput.value;
      markDirty();
    });
    citationsInput.addEventListener('input', () => {
      item.citations = parseCitations(citationsInput.value);
      markDirty('Citation đã thay đổi; hệ thống sẽ kiểm tra khi lưu.');
    });

    questions.append(fragment);
  });
  updateReviewUI();
}

function createRecallSession() {
  return window.RecallSession.create(currentPack.questions.length);
}

function recallStats() {
  return window.RecallSession.stats(recallSession);
}

function appendRecallScore(container, stats) {
  const score = document.createElement('div');
  score.className = 'recall-score';

  const primary = document.createElement('strong');
  primary.textContent = `Đúng ngay lần đầu: ${stats.firstCorrect}/${stats.total}`;
  const detail = document.createElement('span');
  detail.textContent = stats.firstAttempts
    ? ` · ${stats.firstRate}% trên ${stats.firstAttempts} câu đã AI đối chiếu`
    : ' · chưa có câu nào được AI đối chiếu';
  score.append(primary, detail);

  const progress = document.createElement('p');
  progress.textContent = `Đã củng cố: ${stats.mastered}/${stats.total} câu · ${recallSession.queue.length} lượt còn lại`;
  score.append(progress);

  if (stats.firstRate !== null && stats.firstRate < 60) {
    const warning = document.createElement('p');
    warning.className = 'recall-warning';
    warning.textContent = 'Tỉ lệ lượt đầu hiện dưới 60%: câu chưa đạt ngưỡng sẽ quay lại sau một câu khác.';
    score.append(warning);
  }
  container.append(score);
}

function completeRecallAttempt(questionIndex, remembered) {
  try {
    window.RecallSession.record(recallSession, questionIndex, remembered);
  } catch (error) {
    setStatus('error', 'Không thể ghi nhận lượt ôn', error.message);
    return;
  }
  renderQuestions();
}

function renderRecallSession() {
  questions.innerHTML = '';
  if (!recallSession || recallSession.attempts.length !== currentPack.questions.length) {
    recallSession = createRecallSession();
  }

  const stats = recallStats();
  appendRecallScore(questions, stats);

  if (!recallSession.queue.length) {
    const complete = document.createElement('section');
    complete.className = 'recall-complete';
    const title = document.createElement('h4');
    title.textContent = 'Hoàn thành lượt active recall';
    const summary = document.createElement('p');
    const finalRate = stats.total ? Math.round((stats.firstCorrect / stats.total) * 100) : 0;
    summary.textContent = `AI ghi nhận đạt ngưỡng ngay lần đầu ${stats.firstCorrect}/${stats.total} câu (${finalRate}%). ${stats.retryCount ? `Đã ôn lại ${stats.retryCount} lượt chưa đạt.` : 'Không có câu cần ôn lại.'}`;
    const note = document.createElement('p');
    note.className = 'recall-disclaimer';
    note.textContent = 'Đây là mức khớp của câu trả lời với nguồn trong phiên ôn, không phải đánh giá năng lực hay điểm quiz chính thức.';
    const restart = document.createElement('button');
    restart.type = 'button';
    restart.className = 'review-button secondary';
    restart.textContent = 'Làm lại lượt ôn';
    restart.addEventListener('click', () => {
      recallSession = createRecallSession();
      renderQuestions();
    });
    complete.append(title, summary, note, restart);
    questions.append(complete);
    updateReviewUI();
    return;
  }

  const questionIndex = recallSession.queue[0];
  const item = currentPack.questions[questionIndex];
  const isRetry = recallSession.attempts[questionIndex] > 0;
  const card = document.createElement('article');
  card.className = 'question-card recall-card';

  const number = document.createElement('div');
  number.className = 'question-number';
  number.textContent = isRetry ? 'ÔN LẠI' : `CÂU ${questionIndex + 1}`;
  const content = document.createElement('div');
  const title = document.createElement('h4');
  title.textContent = item.question || 'Câu hỏi chưa hoàn tất';
  const prompt = document.createElement('p');
  prompt.className = 'recall-prompt';
  prompt.textContent = 'Nhập câu trả lời của bạn trước khi mở đáp án.';
  const responseInput = document.createElement('textarea');
  responseInput.className = 'learner-response';
  responseInput.rows = 5;
  responseInput.maxLength = 3000;
  responseInput.placeholder = 'Viết lại điều bạn nhớ được...';
  responseInput.setAttribute('aria-label', 'Câu trả lời của bạn');
  const inputMessage = document.createElement('p');
  inputMessage.className = 'recall-input-message';
  const compare = document.createElement('button');
  compare.type = 'button';
  compare.className = 'review-button primary';
  compare.textContent = 'Đối chiếu đáp án';

  const answer = document.createElement('div');
  answer.className = 'answer recall-answer';
  answer.hidden = true;
  const answerLabel = document.createElement('p');
  answerLabel.className = 'answer-label';
  answerLabel.textContent = 'Đáp án gợi ý có căn cứ';
  const answerText = document.createElement('p');
  answerText.textContent = item.answer || 'Chưa có đáp án.';
  const citeList = document.createElement('div');
  citeList.className = 'citation-list';
  item.citations.forEach((code) => citeList.append(citationButton(code)));
  const selfCheck = document.createElement('div');
  selfCheck.className = 'recall-self-check';
  selfCheck.hidden = true;
  const selfCheckLabel = document.createElement('p');
  const continueButton = document.createElement('button');
  continueButton.type = 'button';
  continueButton.className = 'recall-mark correct';
  const retryButton = document.createElement('button');
  retryButton.type = 'button';
  retryButton.className = 'recall-mark incorrect';
  selfCheck.append(selfCheckLabel, continueButton, retryButton);
  answer.append(answerLabel, answerText, citeList, selfCheck);

  compare.addEventListener('click', async () => {
    if (!responseInput.value.trim()) {
      inputMessage.textContent = 'Hãy nhập câu trả lời trước khi đối chiếu đáp án.';
      responseInput.focus();
      return;
    }
    if (dashboardMode === 'teacher' && hasUnsavedChanges) {
      inputMessage.textContent = 'Hãy lưu bản nháp giảng viên trước khi AI đối chiếu câu trả lời với đúng đáp án/citation.';
      return;
    }
    compare.disabled = true;
    compare.textContent = 'AI đang đối chiếu…';
    inputMessage.textContent = 'Chỉ gửi câu hỏi, câu trả lời và các đoạn citation liên quan để đối chiếu.';
    try {
      const response = await apiFetch('/api/recall/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          draft_id: activeReview.draft_id,
          question_index: questionIndex,
          learner_answer: responseInput.value.trim(),
        }),
      });
      const payload = await response.json();
      if (!response.ok) {
        inputMessage.textContent = payload.message || 'Chưa thể tự đối chiếu câu trả lời. Hãy thử lại.';
        return;
      }
      const evaluation = payload.evaluation;
      answer.hidden = false;
      selfCheck.hidden = false;
      selfCheckLabel.textContent = evaluation.passed
        ? `Khớp ${evaluation.match_score}% · đạt ngưỡng ${evaluation.threshold}%`
        : `Khớp ${evaluation.match_score}% · chưa đạt ngưỡng ${evaluation.threshold}%`;
      selfCheckLabel.className = evaluation.passed ? 'evaluation-pass' : 'evaluation-retry';
      const evidence = evaluation.evidence_citations.map((code) => `[${code}]`).join(', ');
      const fallbackNote = payload.metadata?.fallback_used
        ? ` ${payload.metadata.provider === 'openai' ? 'OpenAI' : 'Gemini'} đã được dùng dự phòng.`
        : '';
      inputMessage.textContent = `${evaluation.feedback} Căn cứ: ${evidence}.${fallbackNote}`;
      continueButton.hidden = !evaluation.passed;
      retryButton.hidden = evaluation.passed;
      continueButton.textContent = 'Câu tiếp theo';
      retryButton.textContent = 'Ôn lại sau 1 câu';
      continueButton.onclick = () => completeRecallAttempt(questionIndex, true);
      retryButton.onclick = () => completeRecallAttempt(questionIndex, false);
    } catch (error) {
      inputMessage.textContent = `Không kết nối được backend: ${error.message}`;
    } finally {
      compare.disabled = false;
      compare.textContent = 'Đối chiếu lại bằng AI';
    }
  });

  content.append(title, prompt, responseInput, inputMessage, compare);
  card.append(number, content, answer);
  questions.append(card);
  updateReviewUI();
}

function renderPack(payload) {
  activeTranscript = payload.transcript.file_name;
  currentPack = clone(payload.study_pack);
  activeReview = clone(payload.review);
  editMode = false;
  hasUnsavedChanges = false;
  recallSession = createRecallSession();
  resultContext.textContent = `${payload.transcript.transcript_id} · ${displayTitle(payload.transcript.title)}`;

  renderKeyPoints();
  renderKeywords();
  renderQuestions();

  const warningItems = payload.metadata.warnings || [];
  warnings.hidden = warningItems.length === 0;
  warnings.innerHTML = '';
  warningItems.forEach((warning) => {
    const paragraph = document.createElement('p');
    paragraph.textContent = warning;
    warnings.append(paragraph);
  });

  setReviewMessage('AI đã tạo bản nháp. Giảng viên có thể chỉnh từng câu trước khi duyệt.');
  statusPanel.hidden = true;
  result.hidden = false;
  result.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function saveReview(action = 'draft_saved', details = {}) {
  if (!activeReview || !currentPack) return false;
  saveReviewButton.disabled = true;
  setReviewMessage('Đang kiểm tra cấu trúc và citation...', 'pending');
  try {
    const response = await apiFetch('/api/review', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        draft_id: activeReview.draft_id,
        revision: activeReview.revision,
        study_pack: currentPack,
        action,
        details,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      setReviewMessage(payload.message || 'Không lưu được bản nháp.', 'error');
      return false;
    }
    activeReview = payload.review;
    currentPack = clone(payload.review.study_pack);
    hasUnsavedChanges = false;
    setReviewMessage('Đã lưu bản nháp và kiểm tra citation thành công.', 'success');
    renderQuestions();
    return true;
  } catch (error) {
    setReviewMessage(`Không kết nối được backend: ${error.message}`, 'error');
    return false;
  } finally {
    updateReviewUI();
  }
}

async function approveReview() {
  if (hasUnsavedChanges) {
    const saved = await saveReview('teacher_changes_saved_before_approval');
    if (!saved) return;
  }
  approveReviewButton.disabled = true;
  setReviewMessage('Đang kiểm tra lần cuối trước khi phê duyệt...', 'pending');
  try {
    const response = await apiFetch('/api/review/approve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        draft_id: activeReview.draft_id,
        revision: activeReview.revision,
        study_pack: currentPack,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      setReviewMessage(payload.message || 'Chưa thể phê duyệt.', 'error');
      return;
    }
    activeReview = payload.review;
    currentPack = clone(payload.review.study_pack);
    editMode = false;
    hasUnsavedChanges = false;
    setReviewMessage('Đã phê duyệt. Study Pack hiện ở chế độ chỉ đọc.', 'success');
    renderQuestions();
  } catch (error) {
    setReviewMessage(`Không kết nối được backend: ${error.message}`, 'error');
  } finally {
    approveReviewButton.disabled = false;
    updateReviewUI();
  }
}

async function confirmRegeneration() {
  if (regenerationIndex === null) return;
  const button = document.querySelector('#confirm-regenerate');
  button.disabled = true;
  button.textContent = 'Model đang tạo câu...';
  try {
    const otherQuestions = currentPack.questions.filter((_, index) => index !== regenerationIndex);
    const response = await apiFetch('/api/review/regenerate-question', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        draft_id: activeReview.draft_id,
        current_questions: otherQuestions,
        instruction: document.querySelector('#regenerate-instruction').value,
        question_type: document.querySelector('#question-type').value,
        difficulty: document.querySelector('#question-difficulty').value,
      }),
    });
    const payload = await response.json();
    if (!response.ok) {
      setReviewMessage(payload.message || 'Không tạo lại được câu hỏi.', 'error');
      return;
    }
    currentPack.questions[regenerationIndex] = payload.question;
    const fallbackNote = payload.metadata?.fallback_used
      ? ` ${payload.metadata.provider === 'openai' ? 'OpenAI' : 'Gemini'} đã được dùng dự phòng.`
      : '';
    markDirty(`Model đã tạo câu thay thế và citation đã hợp lệ.${fallbackNote} Hãy lưu bản nháp.`);
    renderQuestions();
    regenerateDialog.close();
  } catch (error) {
    setReviewMessage(`Không kết nối được backend: ${error.message}`, 'error');
  } finally {
    button.disabled = false;
    button.textContent = 'Tạo câu thay thế';
    regenerationIndex = null;
  }
}

function addQuestion() {
  if (!currentPack || currentPack.questions.length >= 5) return;
  const fallbackCitation = currentPack.key_points[0]?.citations?.[0] || '';
  currentPack.questions.push({
    question: '',
    answer: '',
    citations: fallbackCitation ? [fallbackCitation] : [],
  });
  markDirty('Đã thêm một câu trống. Điền nội dung và kiểm tra citation trước khi lưu.');
  renderQuestions();
  questions.lastElementChild?.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

async function generatePack(event) {
  event.preventDefault();
  result.hidden = true;
  setStatus('loading', 'Đang đọc transcript và tạo câu hỏi...', 'Lời gọi này dùng model thật; thường mất vài giây.');
  submitButton.disabled = true;
  submitButton.setAttribute('aria-busy', 'true');
  submitLabel.textContent = 'Đang tạo Study Pack...';

  try {
    const response = await apiFetch('/api/generate', {
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
    if (!payload.review) {
      setStatus('error', 'Không tạo được bản nháp review', 'Backend chưa trả về review draft.');
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
    const response = await apiFetch('/api/transcripts');
    const payload = await response.json();
    if (response.status === 401) {
      accessMessage.textContent = payload.message || 'Mã truy cập chưa đúng.';
      return;
    }
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
accessForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  const token = accessTokenInput.value.trim();
  if (token.length < 24) {
    accessMessage.textContent = 'Mã truy cập phải có ít nhất 24 ký tự.';
    return;
  }
  sessionStorage.setItem(ACCESS_TOKEN_KEY, token);
  accessMessage.textContent = 'Đang xác minh...';
  await loadTranscripts();
  if (transcriptCatalog.length) {
    accessGate.hidden = true;
    accessTokenInput.value = '';
    accessMessage.textContent = '';
  }
});
transcriptSelect.addEventListener('change', updateTranscriptMeta);
regenerate.addEventListener('click', () => form.requestSubmit());
toggleEditButton.addEventListener('click', () => {
  if (dashboardMode !== 'teacher') return;
  editMode = !editMode;
  if (!editMode) recallSession = createRecallSession();
  setReviewMessage(editMode
    ? 'Đang kiểm duyệt: các ô bên dưới là nội dung câu hỏi, đáp án và citation. Bấm “Quay lại lượt active recall” để tự nhập câu trả lời như học viên.'
    : 'Đang làm thử như học viên: có thể nhập câu trả lời, đối chiếu đáp án và citation.');
  renderQuestions();
});
saveReviewButton.addEventListener('click', () => saveReview());
approveReviewButton.addEventListener('click', approveReview);
addQuestionButton.addEventListener('click', addQuestion);
document.querySelector('#confirm-regenerate').addEventListener('click', confirmRegeneration);
document.querySelector('#close-dialog').addEventListener('click', () => citationDialog.close());
document.querySelector('#close-regenerate-dialog').addEventListener('click', () => regenerateDialog.close());
[citationDialog, regenerateDialog].forEach((dialog) => {
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
});

dashboardButtons.forEach((button) => {
  button.addEventListener('click', () => setDashboard(button.dataset.dashboard));
});
setDashboard(new URLSearchParams(window.location.search).get('dashboard'), false);
loadTranscripts();
