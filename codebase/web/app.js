/**
 * 10 mins Study Pack — Frontend Logic for Teacher HITL Workspace & Student Flow.
 */

let currentLesson = null;
let activeTranscript = '';

// --- Tab Switching ---
function switchTab(role) {
  const teacherTab = document.getElementById('tab-teacher');
  const studentTab = document.getElementById('tab-student');
  const teacherView = document.getElementById('teacher-view');
  const studentView = document.getElementById('student-view');

  if (role === 'teacher') {
    teacherTab.classList.add('active');
    studentTab.classList.remove('active');
    teacherView.classList.add('active');
    studentView.classList.remove('active');
    loadTeacherLessons();
  } else {
    studentTab.classList.add('active');
    teacherTab.classList.remove('active');
    studentView.classList.add('active');
    teacherView.classList.remove('active');
    loadTranscripts();
  }
}

// --- File Select UI ---
const pdfFileInput = document.getElementById('pdf-file');
const fileSelectedName = document.getElementById('file-selected-name');

if (pdfFileInput) {
  pdfFileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      fileSelectedName.textContent = `📄 File đã chọn: ${e.target.files[0].name} (${(e.target.files[0].size / 1024 / 1024).toFixed(2)} MB)`;
      fileSelectedName.hidden = false;
    }
  });
}

// --- Teacher Upload & Run Pipeline ---
const teacherUploadForm = document.getElementById('teacher-upload-form');
const teacherProgress = document.getElementById('teacher-progress');
const hitlWorkspace = document.getElementById('hitl-workspace');

if (teacherUploadForm) {
  teacherUploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const lessonCode = document.getElementById('lesson-code').value.trim();
    const lessonTitle = document.getElementById('lesson-title').value.trim();
    const pdfFile = pdfFileInput.files[0];
    const teacherNotes = document.getElementById('teacher-notes').value.trim();

    if (!pdfFile) {
      alert("Vui lòng chọn file Slide PDF!");
      return;
    }

    const formData = new FormData();
    formData.append('file', pdfFile);
    formData.append('lesson_code', lessonCode);
    formData.append('title', lessonTitle);
    formData.append('teacher_notes', teacherNotes);

    teacherProgress.hidden = false;
    hitlWorkspace.hidden = true;
    document.getElementById('publish-alert').hidden = true;
    document.getElementById('btn-run-pipeline').disabled = true;

    try {
      const res = await fetch('/api/teacher/upload-slide', {
        method: 'POST',
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        alert(`Lỗi: ${data.detail || 'Không thể tạo DRAFT bài học'}`);
        return;
      }

      currentLesson = data.lesson;
      renderHitlWorkspace(currentLesson);
      hitlWorkspace.hidden = false;
      hitlWorkspace.scrollIntoView({ behavior: 'smooth' });

    } catch (err) {
      alert(`Lỗi kết nối server: ${err.message}`);
    } finally {
      teacherProgress.hidden = true;
      document.getElementById('btn-run-pipeline').disabled = false;
    }
  });
}

// --- Render HITL Workspace ---
function renderHitlWorkspace(lesson) {
  document.getElementById('hitl-title').value = lesson.title || '';
  
  const summaryInput = document.getElementById('hitl-summary');
  summaryInput.value = lesson.enrich_summary || '';
  updateWordCount(lesson.enrich_summary || '');

  summaryInput.addEventListener('input', (e) => {
    updateWordCount(e.target.value);
  });

  const keywordsList = lesson.keywords || [];
  document.getElementById('hitl-keywords').value = keywordsList.join(', ');

  document.getElementById('hitl-version-badge').textContent = `Version ${lesson.version || 1} (DRAFT)`;

  renderMcqList(lesson.questions || []);
}

function updateWordCount(text) {
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  const badge = document.getElementById('word-count-badge');
  badge.textContent = `${words} từ`;
  if (words >= 300 && words <= 500) {
    badge.className = 'badge badge-success';
  } else {
    badge.className = 'badge';
  }
}

// --- Render MCQ List ---
function renderMcqList(questions) {
  const container = document.getElementById('mcq-list-container');
  container.innerHTML = '';

  let approvedCount = 0;

  questions.forEach((q, idx) => {
    if (q.is_approved) approvedCount++;

    const card = document.createElement('div');
    card.className = `mcq-card-edit ${q.is_approved ? 'approved' : ''}`;
    card.dataset.id = q.id || `temp_${idx}`;

    card.innerHTML = `
      <div class="mcq-header-row">
        <span class="mcq-num-badge">Câu ${idx + 1} / ${questions.length}</span>
        <div class="mcq-actions-top">
          <label class="approve-checkbox-label">
            <input type="checkbox" class="mcq-approve-chk" ${q.is_approved ? 'checked' : ''} onchange="toggleApprove('${q.id || idx}', this.checked)">
            <span>${q.is_approved ? '✅ Đã Duyệt' : 'Chưa Duyệt'}</span>
          </label>
          <button type="button" class="btn btn-sm btn-outline" onclick="openRegenMcqModal('${q.id}')">
            🔄 Sinh lại câu này
          </button>
        </div>
      </div>

      <div class="form-group mb-2">
        <label>Nội dung câu hỏi</label>
        <input type="text" class="mcq-q-text" value="${escapeHtml(q.question_text || '')}">
      </div>

      <div class="options-grid">
        <div class="option-input-group">
          <span class="option-prefix">A.</span>
          <input type="text" class="mcq-opt-A" value="${escapeHtml(q.options?.A || '')}">
        </div>
        <div class="option-input-group">
          <span class="option-prefix">B.</span>
          <input type="text" class="mcq-opt-B" value="${escapeHtml(q.options?.B || '')}">
        </div>
        <div class="option-input-group">
          <span class="option-prefix">C.</span>
          <input type="text" class="mcq-opt-C" value="${escapeHtml(q.options?.C || '')}">
        </div>
        <div class="option-input-group">
          <span class="option-prefix">D.</span>
          <input type="text" class="mcq-opt-D" value="${escapeHtml(q.options?.D || '')}">
        </div>
      </div>

      <div class="correct-selector-row">
        <label><strong>Đáp án đúng:</strong></label>
        <select class="mcq-correct-sel">
          <option value="A" ${q.correct_option === 'A' ? 'selected' : ''}>A</option>
          <option value="B" ${q.correct_option === 'B' ? 'selected' : ''}>B</option>
          <option value="C" ${q.correct_option === 'C' ? 'selected' : ''}>C</option>
          <option value="D" ${q.correct_option === 'D' ? 'selected' : ''}>D</option>
        </select>
      </div>

      <div class="form-group">
        <label>Giải thích chi tiết</label>
        <input type="text" class="mcq-explanation" value="${escapeHtml(q.explanation || '')}">
      </div>
    `;

    container.appendChild(card);
  });

  document.getElementById('approved-count').textContent = `${approvedCount}/${questions.length} Đã duyệt`;
}

function toggleApprove(qId, isChecked) {
  if (!currentLesson) return;
  const q = currentLesson.questions.find(item => item.id === qId);
  if (q) {
    q.is_approved = isChecked;
  }
  renderMcqList(currentLesson.questions);
}

// --- Collect Edits ---
function collectEdits() {
  if (!currentLesson) return null;

  const title = document.getElementById('hitl-title').value.trim();
  const summary = document.getElementById('hitl-summary').value.trim();
  const keywordsStr = document.getElementById('hitl-keywords').value.trim();
  const keywords = keywordsStr ? keywordsStr.split(',').map(k => k.trim()).filter(Boolean) : [];

  const cards = document.querySelectorAll('.mcq-card-edit');
  const updatedQuestions = [];

  cards.forEach(card => {
    const qId = card.dataset.id;
    const qText = card.querySelector('.mcq-q-text').value.trim();
    const optA = card.querySelector('.mcq-opt-A').value.trim();
    const optB = card.querySelector('.mcq-opt-B').value.trim();
    const optC = card.querySelector('.mcq-opt-C').value.trim();
    const optD = card.querySelector('.mcq-opt-D').value.trim();
    const correctOpt = card.querySelector('.mcq-correct-sel').value;
    const explanation = card.querySelector('.mcq-explanation').value.trim();
    const isApproved = card.querySelector('.mcq-approve-chk').checked;

    updatedQuestions.push({
      id: qId,
      question_text: qText,
      options: { A: optA, B: optB, C: optC, D: optD },
      correct_option: correctOpt,
      explanation: explanation,
      is_approved: isApproved,
    });
  });

  currentLesson.title = title;
  currentLesson.enrich_summary = summary;
  currentLesson.keywords = keywords;
  currentLesson.questions = updatedQuestions;

  return {
    lesson_id: currentLesson.id,
    title: title,
    enrich_summary: summary,
    keywords: keywords,
    questions: updatedQuestions,
  };
}

// --- Save Draft Review ---
async function saveDraftReview() {
  const payload = collectEdits();
  if (!payload) return;

  try {
    const res = await fetch('/api/teacher/review', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await res.json();
    if (res.ok) {
      alert("Đã lưu bản nháp thành công!");
    } else {
      alert(`Lỗi lưu bản nháp: ${data.detail || 'Thao tác thất bại'}`);
    }
  } catch (err) {
    alert(`Lỗi kết nối: ${err.message}`);
  }
}

// --- Publish Lesson ---
async function publishLesson() {
  const edits = collectEdits();
  if (!edits) return;

  const btnPublish = document.getElementById('btn-publish');
  btnPublish.disabled = true;
  btnPublish.innerHTML = '<span>⏳ Đang xuất bản & Sync Vector DB...</span>';

  try {
    // 1. Save edits
    await fetch('/api/teacher/review', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(edits),
    });

    // 2. Call Publish endpoint
    const res = await fetch(`/api/teacher/publish/${currentLesson.id}`, {
      method: 'POST',
    });

    const data = await res.json();
    if (!res.ok) {
      alert(`Lỗi xuất bản: ${data.detail || 'Thao tác thất bại'}`);
      return;
    }

    // Success alert UI
    const alertBox = document.getElementById('publish-alert');
    document.getElementById('publish-alert-title').textContent = data.message;
    document.getElementById('publish-alert-desc').textContent = 
      `Vector DB Sync Status: ${data.vector_db_sync.status} (${data.vector_db_sync.indexed_chunks} chunks đã được lưu vào ChromaDB).`;
    alertBox.hidden = false;
    alertBox.scrollIntoView({ behavior: 'smooth' });

    loadTeacherLessons();

  } catch (err) {
    alert(`Lỗi kết nối: ${err.message}`);
  } finally {
    btnPublish.disabled = false;
    btnPublish.innerHTML = '<span>✅ Approve & Publish (Sync Vector DB)</span>';
  }
}

// --- Regenerate Single MCQ ---
function openRegenMcqModal(qId) {
  document.getElementById('regen-q-id').value = qId;
  document.getElementById('regen-instruction').value = '';
  document.getElementById('regen-mcq-dialog').showModal();
}

async function confirmRegenerateMcq() {
  const qId = document.getElementById('regen-q-id').value;
  const customInst = document.getElementById('regen-instruction').value.trim();
  document.getElementById('regen-mcq-dialog').close();

  if (!currentLesson || !qId) return;

  try {
    const res = await fetch('/api/teacher/regenerate-mcq', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lesson_id: currentLesson.id,
        question_id: qId,
        custom_instruction: customInst,
      }),
    });

    const data = await res.json();
    if (res.ok && data.question) {
      const idx = currentLesson.questions.findIndex(q => q.id === qId);
      if (idx !== -1) {
        currentLesson.questions[idx] = data.question;
        renderMcqList(currentLesson.questions);
      }
    } else {
      alert(`Không thể tạo lại câu hỏi: ${data.detail || ''}`);
    }
  } catch (err) {
    alert(`Lỗi: ${err.message}`);
  }
}

// --- Load Published Lessons Table ---
async function loadTeacherLessons() {
  const tbody = document.getElementById('teacher-lessons-tbody');
  if (!tbody) return;

  try {
    const res = await fetch('/api/teacher/lessons');
    const data = await res.json();
    tbody.innerHTML = '';

    if (!data.lessons || data.lessons.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" class="text-center">Chưa có bài học nào được khởi tạo.</td></tr>';
      return;
    }

    data.lessons.forEach(l => {
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><strong>${escapeHtml(l.lesson_code)}</strong></td>
        <td>${escapeHtml(l.title)}</td>
        <td><span class="badge">v${l.version}</span></td>
        <td><span class="badge ${l.status === 'PUBLISHED' ? 'badge-success' : ''}">${l.status}</span></td>
        <td>${l.questions_count} câu</td>
        <td>
          <button class="btn btn-sm btn-outline" onclick="loadLessonForReview('${l.id}')">✏️ Xem / Chỉnh sửa</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Lỗi tải danh sách: ${err.message}</td></tr>`;
  }
}

async function loadLessonForReview(lessonId) {
  try {
    const res = await fetch(`/api/teacher/lesson/${lessonId}`);
    const data = await res.json();
    if (res.ok && data.lesson) {
      currentLesson = data.lesson;
      renderHitlWorkspace(currentLesson);
      hitlWorkspace.hidden = false;
      hitlWorkspace.scrollIntoView({ behavior: 'smooth' });
    }
  } catch (err) {
    alert(`Không tải được chi tiết bài học: ${err.message}`);
  }
}

// --- Helper Functions ---
function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

// --- Student Flow Handlers ---
const studentForm = document.getElementById('student-generate-form');
const transcriptSelect = document.getElementById('transcript-select');
const studentStatus = document.getElementById('student-status');
const studentResult = document.getElementById('student-result');

if (studentForm) {
  studentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    studentResult.hidden = true;
    setStudentStatus('loading', 'Đang nén transcript và tạo Study Pack 10 phút...');

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          transcript: transcriptSelect.value,
          objective: document.getElementById('objective').value,
        }),
      });
      const payload = await response.json();
      if (!response.ok) {
        setStudentStatus('error', 'Chưa thể tạo Study Pack', payload.detail || 'Backend trả về lỗi.');
        return;
      }
      renderStudentPack(payload);
    } catch (error) {
      setStudentStatus('error', 'Không kết nối được backend', error.message);
    }
  });
}

function setStudentStatus(kind, title, detail = '') {
  studentStatus.hidden = false;
  studentStatus.className = `status-panel alert ${kind === 'error' ? 'alert-danger' : 'alert-info'}`;
  studentStatus.innerHTML = `<strong>${title}</strong>${detail ? `<p>${detail}</p>` : ''}`;
}

function renderStudentPack(payload) {
  const pack = payload.study_pack;
  const keyPointsEl = document.getElementById('key-points');
  const keywordsEl = document.getElementById('keywords');
  const questionsEl = document.getElementById('questions');

  keyPointsEl.innerHTML = '';
  keywordsEl.innerHTML = '';
  questionsEl.innerHTML = '';

  if (pack.key_points) {
    pack.key_points.forEach((item) => {
      const li = document.createElement('li');
      li.textContent = item.content || item;
      keyPointsEl.appendChild(li);
    });
  }

  if (pack.keywords) {
    pack.keywords.forEach((kw) => {
      const chip = document.createElement('span');
      chip.className = 'badge';
      chip.textContent = kw;
      keywordsEl.appendChild(chip);
    });
  }

  if (pack.questions) {
    pack.questions.forEach((q, i) => {
      const div = document.createElement('div');
      div.className = 'card';
      div.innerHTML = `
        <h4>Câu ${i + 1}: ${escapeHtml(q.question || q.question_text || '')}</h4>
        <p><strong>Đáp án:</strong> ${escapeHtml(q.answer || q.correct_option || '')}</p>
      `;
      questionsEl.appendChild(div);
    });
  }

  studentStatus.hidden = true;
  studentResult.hidden = false;
}

async function loadTranscripts() {
  if (!transcriptSelect) return;
  try {
    const res = await fetch('/api/transcripts');
    const data = await res.json();
    transcriptSelect.innerHTML = '<option value="">-- Chọn bài học / transcript --</option>';
    if (data.transcripts) {
      data.transcripts.forEach(t => {
        const opt = document.createElement('option');
        opt.value = t;
        opt.textContent = t;
        transcriptSelect.appendChild(opt);
      });
    }
  } catch (err) {
    transcriptSelect.innerHTML = '<option value="">Không tải được danh sách</option>';
  }
}

// Initial Load
document.addEventListener('DOMContentLoaded', () => {
  loadTeacherLessons();
});
