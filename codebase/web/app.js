/**
 * 10 mins Study Pack — Frontend Logic for Teacher HITL Workspace & Student Flow.
 * Full integration with Socratic Tutor AI & Feynman Reverse-Role Mode.
 */

let currentLesson = null;
let currentStudentPack = null;
let activeFeynmanSessionId = null;
let activeSocraticSessionId = null;

// --- Tab Switching ---
function switchTab(role) {
  const teacherTab = document.getElementById('tab-teacher');
  const studentTab = document.getElementById('tab-student');
  const teacherView = document.getElementById('teacher-view');
  const studentView = document.getElementById('student-view');

  if (role === 'teacher') {
    if (teacherTab) teacherTab.classList.add('active');
    if (studentTab) studentTab.classList.remove('active');
    if (teacherView) teacherView.classList.add('active');
    if (studentView) studentView.classList.remove('active');
    loadTeacherLessons();
  } else {
    if (studentTab) studentTab.classList.add('active');
    if (teacherTab) teacherTab.classList.remove('active');
    if (studentView) studentView.classList.add('active');
    if (teacherView) teacherView.classList.remove('active');
    loadPublishedLessonsForStudent();
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

function renderMarkdown(text) {
  if (!text || typeof text !== 'string') return '';

  let cleanedText = text.trim();

  // Remove markdown codeblock fence wrappers (e.g. ```markdown ... ```) if pasted inside notes
  cleanedText = cleanedText
    .replace(/^```(?:markdown|md)?\s*\n/gim, '')
    .replace(/\n```\s*$/gim, '')
    .replace(/```markdown\n?/gi, '')
    .replace(/```md\n?/gi, '');

  // Use marked.js if available
  if (typeof marked !== 'undefined') {
    try {
      if (typeof marked.parse === 'function') {
        return marked.parse(cleanedText);
      } else if (typeof marked === 'function') {
        return marked(cleanedText);
      }
    } catch (err) {
      console.warn("marked parsing warning:", err);
    }
  }

  // Fallback regex markdown parser
  let raw = escapeHtml(cleanedText);
  raw = raw.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
  raw = raw.replace(/`([^`]+)`/g, '<code>$1</code>');
  raw = raw.replace(/^### (.*$)/gim, '<h3>$1</h3>');
  raw = raw.replace(/^## (.*$)/gim, '<h2>$1</h2>');
  raw = raw.replace(/^# (.*$)/gim, '<h1>$1</h1>');
  raw = raw.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  raw = raw.replace(/\*(.*?)\*/g, '<em>$1</em>');
  raw = raw.replace(/^&gt;\s?(.*$)/gim, '<blockquote>$1</blockquote>');
  raw = raw.replace(/^\s*[\-\*]\s+(.*$)/gim, '<li>$1</li>');
  raw = raw.replace(/(<li>.*<\/li>)/gim, '<ul>$1</ul>');
  raw = raw.replace(/\n\n/g, '</p><p>');
  raw = raw.replace(/\n/g, '<br>');

  return `<p>${raw}</p>`;
}


// =========================================================================
// ========================= TEACHER WORKSPACE =============================
// =========================================================================

function handleTeacherUpload(e) {
  e.preventDefault();

  const pdfFileInput = document.getElementById('pdf-file');
  const lessonCode = document.getElementById('lesson-code').value.trim();
  const lessonTitle = document.getElementById('lesson-title').value.trim();
  const pdfFile = pdfFileInput ? pdfFileInput.files[0] : null;
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

  const teacherProgress = document.getElementById('teacher-progress');
  const hitlWorkspace = document.getElementById('hitl-workspace');
  const btnRun = document.getElementById('btn-run-pipeline');

  if (teacherProgress) teacherProgress.hidden = false;
  if (hitlWorkspace) hitlWorkspace.hidden = true;
  const publishAlert = document.getElementById('publish-alert');
  if (publishAlert) publishAlert.hidden = true;
  if (btnRun) btnRun.disabled = true;

  fetch('/api/teacher/upload-slide', {
    method: 'POST',
    body: formData,
  })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
      if (!ok) {
        alert(`Lỗi: ${data.detail || 'Không thể tạo DRAFT bài học'}`);
        return;
      }

      currentLesson = data.lesson;
      renderHitlWorkspace(currentLesson);
      if (hitlWorkspace) {
        hitlWorkspace.hidden = false;
        hitlWorkspace.scrollIntoView({ behavior: 'smooth' });
      }
    })
    .catch(err => {
      alert(`Lỗi kết nối server: ${err.message}`);
    })
    .finally(() => {
      if (teacherProgress) teacherProgress.hidden = true;
      if (btnRun) btnRun.disabled = false;
    });
}

function renderHitlWorkspace(lesson) {
  const titleInput = document.getElementById('hitl-title');
  const summaryInput = document.getElementById('hitl-summary');
  const keywordsInput = document.getElementById('hitl-keywords');
  const versionBadge = document.getElementById('hitl-version-badge');

  if (titleInput) titleInput.value = lesson.title || '';
  if (summaryInput) {
    summaryInput.value = lesson.enrich_summary || '';
    updateWordCount(lesson.enrich_summary || '');
    summaryInput.oninput = (e) => updateWordCount(e.target.value);
  }

  if (keywordsInput) {
    const keywordsList = lesson.keywords || [];
    keywordsInput.value = keywordsList.join(', ');
  }

  if (versionBadge) {
    versionBadge.textContent = `Version ${lesson.version || 1} (DRAFT)`;
  }

  renderMcqList(lesson.questions || []);
}

function updateWordCount(text) {
  const words = text.trim() ? text.trim().split(/\s+/).length : 0;
  const badge = document.getElementById('word-count-badge');
  if (badge) {
    badge.textContent = `${words} từ`;
    if (words >= 300 && words <= 500) {
      badge.className = 'badge badge-success';
    } else {
      badge.className = 'badge';
    }
  }
}

function renderMcqList(questions) {
  const container = document.getElementById('mcq-list-container');
  if (!container) return;
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

  const countBadge = document.getElementById('approved-count');
  if (countBadge) countBadge.textContent = `${approvedCount}/${questions.length} Đã duyệt`;
}

function toggleApprove(qId, isChecked) {
  if (!currentLesson) return;
  const q = currentLesson.questions.find(item => item.id === qId);
  if (q) {
    q.is_approved = isChecked;
  }
  renderMcqList(currentLesson.questions);
}

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

async function publishLesson() {
  const edits = collectEdits();
  if (!edits) return;

  const btnPublish = document.getElementById('btn-publish');
  if (btnPublish) {
    btnPublish.disabled = true;
    btnPublish.innerHTML = '<span>⏳ Đang xuất bản & Sync Vector DB...</span>';
  }

  try {
    await fetch('/api/teacher/review', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(edits),
    });

    const res = await fetch(`/api/teacher/publish/${currentLesson.id}`, {
      method: 'POST',
    });

    const data = await res.json();
    if (!res.ok) {
      alert(`Lỗi xuất bản: ${data.detail || 'Thao tác thất bại'}`);
      return;
    }

    const alertBox = document.getElementById('publish-alert');
    const alertTitle = document.getElementById('publish-alert-title');
    const alertDesc = document.getElementById('publish-alert-desc');
    if (alertTitle) alertTitle.textContent = data.message;
    if (alertDesc) alertDesc.textContent = `Vector DB Sync Status: ${data.vector_db_sync.status} (${data.vector_db_sync.indexed_chunks} chunks đã được lưu vào ChromaDB).`;
    if (alertBox) {
      alertBox.hidden = false;
      alertBox.scrollIntoView({ behavior: 'smooth' });
    }

    loadTeacherLessons();

  } catch (err) {
    alert(`Lỗi kết nối: ${err.message}`);
  } finally {
    if (btnPublish) {
      btnPublish.disabled = false;
      btnPublish.innerHTML = '<span>✅ Approve & Publish (Sync Vector DB)</span>';
    }
  }
}

function openRegenMcqModal(qId) {
  const qIdInput = document.getElementById('regen-q-id');
  const instInput = document.getElementById('regen-instruction');
  const dialog = document.getElementById('regen-mcq-dialog');

  if (qIdInput) qIdInput.value = qId;
  if (instInput) instInput.value = '';
  if (dialog) dialog.showModal();
}

async function confirmRegenerateMcq() {
  const qId = document.getElementById('regen-q-id').value;
  const customInst = document.getElementById('regen-instruction').value.trim();
  const dialog = document.getElementById('regen-mcq-dialog');
  if (dialog) dialog.close();

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
      const workspace = document.getElementById('hitl-workspace');
      if (workspace) {
        workspace.hidden = false;
        workspace.scrollIntoView({ behavior: 'smooth' });
      }
    }
  } catch (err) {
    alert(`Không tải được chi tiết bài học: ${err.message}`);
  }
}


// =========================================================================
// ========================= STUDENT FLOW LOGIC ============================
// =========================================================================

// 1. Load Published Lessons for Student Dropdown
async function loadPublishedLessonsForStudent() {
  const selectEl = document.getElementById('student-lesson-select');
  if (!selectEl) {
    console.warn("Element #student-lesson-select not found yet.");
    return;
  }

  selectEl.innerHTML = '<option value="">Đang tải danh sách bài học...</option>';

  try {
    const res = await fetch('/api/student/lessons');
    const data = await res.json();
    console.log("Student lessons loaded:", data);

    let list = data.lessons || [];

    // Fallback to teacher lessons if no published lessons
    if (list.length === 0) {
      const teacherRes = await fetch('/api/teacher/lessons');
      const teacherData = await teacherRes.json();
      list = teacherData.lessons || [];
    }

    selectEl.innerHTML = '';

    if (list.length === 0) {
      selectEl.innerHTML = '<option value="">Chưa có bài học nào được xuất bản từ Giảng viên.</option>';
      return;
    }

    selectEl.innerHTML = '<option value="">-- Chọn một bài học để bắt đầu --</option>';
    list.forEach(l => {
      const opt = document.createElement('option');
      opt.value = l.lesson_code || l.id;
      opt.textContent = `[${l.lesson_code}] ${l.title} (v${l.version} - ${l.questions_count} câu MCQ)`;
      selectEl.appendChild(opt);
    });

  } catch (err) {
    console.error("Lỗi loadPublishedLessonsForStudent:", err);
    selectEl.innerHTML = `<option value="">Lỗi tải danh sách: ${err.message}</option>`;
  }
}

// 2. Open Student Study Pack
async function openStudentStudyPack(lessonCode) {
  const btnOpen = document.getElementById('btn-open-pack');
  if (btnOpen) btnOpen.disabled = true;

  try {
    const res = await fetch(`/api/student/lessons/${lessonCode}`);
    const data = await res.json();

    if (!res.ok) {
      alert(`Lỗi: ${data.detail || 'Không tải được bài học.'}`);
      return;
    }

    currentStudentPack = data;
    renderStudentStudyPack(currentStudentPack);
    const workspace = document.getElementById('student-pack-workspace');
    if (workspace) {
      workspace.hidden = false;
      workspace.scrollIntoView({ behavior: 'smooth' });
    }

  } catch (err) {
    alert(`Lỗi kết nối: ${err.message}`);
  } finally {
    if (btnOpen) btnOpen.disabled = false;
  }
}

// 3. Render Student Study Pack Components
function renderStudentStudyPack(pack) {
  const titleEl = document.getElementById('sp-title');
  const codeSubEl = document.getElementById('sp-code-sub');
  const versionEl = document.getElementById('sp-version-badge');
  const pdfLink = document.getElementById('sp-pdf-link');
  const kwContainer = document.getElementById('sp-keywords-container');
  const summaryEl = document.getElementById('sp-enrich-summary');
  const notesCard = document.getElementById('sp-teacher-notes-card');
  const notesEl = document.getElementById('sp-teacher-notes');

  if (titleEl) titleEl.textContent = pack.title || pack.lesson_code;
  if (codeSubEl) codeSubEl.textContent = `Mã bài học: ${pack.lesson_code}`;
  if (versionEl) versionEl.textContent = `Version ${pack.version || 1}`;

  if (pdfLink) {
    if (pack.pdf_url) {
      pdfLink.href = pack.pdf_url;
      pdfLink.hidden = false;
    } else {
      pdfLink.hidden = true;
    }
  }

  if (kwContainer) {
    kwContainer.innerHTML = '';
    (pack.keywords || []).forEach(kw => {
      const chip = document.createElement('span');
      chip.className = 'badge';
      chip.textContent = kw;
      kwContainer.appendChild(chip);
    });
  }

  if (summaryEl) summaryEl.innerHTML = renderMarkdown(pack.enrich_summary || 'Chưa có nội dung tóm tắt.');

  if (notesCard && notesEl) {
    if (pack.teacher_notes && pack.teacher_notes.trim()) {
      notesEl.innerHTML = renderMarkdown(pack.teacher_notes);
      notesCard.hidden = false;
    } else {
      notesCard.hidden = true;
    }
  }

  renderStudentQuickQuiz(pack.questions || []);
  switchStudentSubTab('summary');
}

// 4. Subtab Switcher
function switchStudentSubTab(tabName) {
  const tabs = ['summary', 'quiz', 'feynman'];
  tabs.forEach(t => {
    const btn = document.getElementById(`subtab-${t}`);
    const content = document.getElementById(`student-tab-${t}`);
    if (btn && content) {
      if (t === tabName) {
        btn.classList.add('active');
        content.classList.add('active');
      } else {
        btn.classList.remove('active');
        content.classList.remove('active');
      }
    }
  });
}

// 5. Render Quick Quiz for Student
function renderStudentQuickQuiz(questions) {
  const container = document.getElementById('quiz-questions-container');
  const scoreBadge = document.getElementById('quiz-score-badge');
  if (!container) return;
  container.innerHTML = '';

  if (scoreBadge) scoreBadge.hidden = true;

  if (questions.length === 0) {
    container.innerHTML = '<p class="text-muted">Chưa có câu hỏi trắc nghiệm nào cho bài học này.</p>';
    return;
  }

  questions.forEach((q, idx) => {
    const card = document.createElement('div');
    card.className = 'quiz-q-card';
    card.id = `quiz-card-${q.id || idx}`;

    const options = q.options || {};
    let optionsHtml = '';

    ['A', 'B', 'C', 'D'].forEach(optKey => {
      if (options[optKey]) {
        optionsHtml += `
          <label class="option-label">
            <input type="radio" name="q_${q.id || idx}" value="${optKey}">
            <span><strong>${optKey}.</strong> ${escapeHtml(options[optKey])}</span>
          </label>
        `;
      }
    });

    card.innerHTML = `
      <div class="quiz-q-title">Câu ${idx + 1}: ${escapeHtml(q.question_text)}</div>
      <div class="options-list">
        ${optionsHtml}
      </div>
      <div id="quiz-result-${q.id || idx}" class="quiz-result-box" hidden></div>
    `;

    container.appendChild(card);
  });
}

// 6. Handle Quiz Submission & Grading
function handleQuizSubmit(e) {
  e.preventDefault();
  if (!currentStudentPack || !currentStudentPack.questions) return;

  const quizForm = document.getElementById('quiz-form');
  const questions = currentStudentPack.questions;
  let correctCount = 0;

  questions.forEach((q, idx) => {
    const qKey = q.id || idx;
    const card = document.getElementById(`quiz-card-${qKey}`);
    const resultBox = document.getElementById(`quiz-result-${qKey}`);
    const selectedRadio = quizForm ? quizForm.querySelector(`input[name="q_${qKey}"]:checked`) : null;

    const userChoice = selectedRadio ? selectedRadio.value : null;
    const isCorrect = userChoice === q.correct_option;

    if (card) card.className = `quiz-q-card ${isCorrect ? 'correct' : 'incorrect'}`;

    if (resultBox) {
      if (isCorrect) {
        correctCount++;
        resultBox.className = 'quiz-result-box alert alert-success mt-3';
        resultBox.innerHTML = `
          <strong>✅ Chính xác!</strong>
          <p class="mt-1">${escapeHtml(q.explanation || 'Xuất sắc!')}</p>
        `;
      } else {
        resultBox.className = 'quiz-result-box alert alert-danger mt-3';
        resultBox.innerHTML = `
          <strong>❌ Chưa chính xác!</strong>
          <p class="mt-1">Đáp án đúng chính thức: <strong>${q.correct_option}</strong></p>
          <p class="text-muted mt-1">${escapeHtml(q.explanation || '')}</p>
          <button type="button" class="btn-socratic mt-2" onclick="openSocraticModal('${currentStudentPack.lesson_code}', '${q.id}', '${userChoice || 'N/A'}', '${escapeHtml(q.question_text)}')">
            🤖 Hỏi AI Socratic Giải Thích Thêm ➔
          </button>
        `;
      }
      resultBox.hidden = false;
    }
  });

  const scoreBadge = document.getElementById('quiz-score-badge');
  const scoreText = document.getElementById('score-text');
  if (scoreText) scoreText.textContent = `${correctCount}/${questions.length} (${Math.round((correctCount / questions.length) * 100)}%)`;
  if (scoreBadge) {
    scoreBadge.hidden = false;
    scoreBadge.scrollIntoView({ behavior: 'smooth' });
  }
}


// =========================================================================
// ==================== CHATBOT 1: SOCRATIC TUTOR AGENT ====================
// =========================================================================

function openSocraticModal(lessonCode, questionId, userOption, questionText) {
  const dialog = document.getElementById('socratic-dialog');
  document.getElementById('soc-lesson-code').value = lessonCode;
  document.getElementById('soc-question-id').value = questionId || '';
  document.getElementById('soc-user-option').value = userOption || 'N/A';

  activeSocraticSessionId = `socratic_${Date.now()}`;
  document.getElementById('soc-session-id').value = activeSocraticSessionId;

  document.getElementById('soc-q-title').textContent = `Giải thích câu hỏi trắc nghiệm`;
  document.getElementById('soc-q-sub').textContent = `"${questionText}" (Lựa chọn của bạn: ${userOption})`;

  const list = document.getElementById('socratic-messages-list');
  if (list) {
    list.innerHTML = `
      <div class="msg-bubble msg-ai">
        <strong>Trợ giảng Socratic:</strong><br>
        Chào bạn! Tôi đang xem lại câu hỏi này. Bạn có muốn hỏi thêm điều gì cụ thể hoặc muốn tôi giải thích bản chất khái niệm chưa đúng không?
      </div>
    `;
  }

  if (dialog) dialog.showModal();
}

function closeSocraticModal() {
  const dialog = document.getElementById('socratic-dialog');
  if (dialog) dialog.close();
}

function handleSocraticChatSubmit(e) {
  e.preventDefault();

  const lessonCode = document.getElementById('soc-lesson-code').value;
  const questionId = document.getElementById('soc-question-id').value;
  const userOption = document.getElementById('soc-user-option').value;
  const sessionId = document.getElementById('soc-session-id').value;
  const userInputEl = document.getElementById('soc-user-input');
  const userInput = userInputEl ? userInputEl.value.trim() : '';

  if (!userInput) return;

  const list = document.getElementById('socratic-messages-list');
  if (!list) return;

  const userBubble = document.createElement('div');
  userBubble.className = 'msg-bubble msg-user';
  userBubble.textContent = userInput;
  list.appendChild(userBubble);

  if (userInputEl) userInputEl.value = '';
  list.scrollTop = list.scrollHeight;

  const loadingBubble = document.createElement('div');
  loadingBubble.className = 'msg-bubble msg-ai';
  loadingBubble.innerHTML = '<em>Trợ giảng Socratic đang suy nghĩ và tra cứu Vector DB...</em>';
  list.appendChild(loadingBubble);
  list.scrollTop = list.scrollHeight;

  fetch('/api/student/chat/explain', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      lesson_code: lessonCode,
      question_id: questionId,
      user_selected_option: userOption,
      user_message: userInput,
      session_id: sessionId,
    }),
  })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
      if (ok && data.reply) {
        loadingBubble.innerHTML = `<strong>Trợ giảng Socratic:</strong><div class="markdown-body mt-1">${renderMarkdown(data.reply)}</div>`;
      } else {
        loadingBubble.innerHTML = `<strong>Lỗi:</strong> ${data.detail || 'Không nhận được phản hồi.'}`;
      }
    })
    .catch(err => {
      loadingBubble.innerHTML = `<strong>Lỗi kết nối:</strong> ${err.message}`;
    })
    .finally(() => {
      list.scrollTop = list.scrollHeight;
    });
}


// =========================================================================
// ================= CHATBOT 2: FEYNMAN REVERSE-ROLE AGENT =================
// =========================================================================

async function startFeynmanChat() {
  if (!currentStudentPack) {
    alert("Vui lòng chọn bài học trước!");
    return;
  }

  const list = document.getElementById('feynman-messages-list');
  const container = document.getElementById('feynman-chat-container');

  if (list) list.innerHTML = '<div class="msg-bubble msg-ai"><em>Đang khởi tạo Học sinh AI tò mò...</em></div>';
  if (container) container.hidden = false;

  try {
    const res = await fetch('/api/student/chat/feynman/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lesson_code: currentStudentPack.lesson_code,
      }),
    });

    const data = await res.json();
    if (res.ok && data.session_id) {
      activeFeynmanSessionId = data.session_id;
      if (list) {
        list.innerHTML = `
          <div class="msg-bubble msg-ai">
            <strong>Học sinh AI (Tò mò):</strong><br>
            ${escapeHtml(data.initial_message).replace(/\n/g, '<br>')}
          </div>
        `;
      }
    } else {
      if (list) list.innerHTML = `<div class="msg-bubble msg-ai text-danger">Lỗi: ${data.detail || 'Không thể khởi tạo.'}</div>`;
    }

  } catch (err) {
    if (list) list.innerHTML = `<div class="msg-bubble msg-ai text-danger">Lỗi kết nối: ${err.message}</div>`;
  }
}

function handleFeynmanChatSubmit(e) {
  e.preventDefault();

  const inputEl = document.getElementById('feynman-input');
  const list = document.getElementById('feynman-messages-list');
  const btnSend = document.getElementById('btn-send-feynman');
  const studentAnswer = inputEl ? inputEl.value.trim() : '';

  if (!studentAnswer || !activeFeynmanSessionId || !currentStudentPack) return;

  const userBubble = document.createElement('div');
  userBubble.className = 'msg-bubble msg-user';
  userBubble.innerHTML = `<strong>Thầy giáo (Bạn):</strong><br>${escapeHtml(studentAnswer).replace(/\n/g, '<br>')}`;
  if (list) list.appendChild(userBubble);

  if (inputEl) inputEl.value = '';
  if (list) list.scrollTop = list.scrollHeight;

  const aiBubble = document.createElement('div');
  aiBubble.className = 'msg-bubble msg-ai';
  aiBubble.innerHTML = '<em>Học sinh AI đang lắng nghe và suy ngẫm...</em>';
  if (list) list.appendChild(aiBubble);
  if (list) list.scrollTop = list.scrollHeight;

  if (btnSend) btnSend.disabled = true;

  fetch('/api/student/chat/feynman/respond', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: activeFeynmanSessionId,
      lesson_code: currentStudentPack.lesson_code,
      student_answer: studentAnswer,
    }),
  })
    .then(res => res.json().then(data => ({ ok: res.ok, data })))
    .then(({ ok, data }) => {
      if (ok && data.reply) {
        aiBubble.innerHTML = `<strong>Học sinh AI (Tò mò):</strong><div class="markdown-body mt-1">${renderMarkdown(data.reply)}</div>`;
      } else {
        aiBubble.innerHTML = `<strong>Lỗi:</strong> ${data.detail || 'Không nhận được phản hồi.'}`;
      }
    })
    .catch(err => {
      aiBubble.innerHTML = `<strong>Lỗi kết nối:</strong> ${err.message}`;
    })
    .finally(() => {
      if (btnSend) btnSend.disabled = false;
      if (list) list.scrollTop = list.scrollHeight;
    });
}


// =========================================================================
// ======================== INITIAL DOM EVENT LOADER =======================
// =========================================================================

document.addEventListener('DOMContentLoaded', () => {
  console.log("🚀 10M Study Pack Web App initialized.");

  // File Upload listener
  const pdfFileInput = document.getElementById('pdf-file');
  const fileSelectedName = document.getElementById('file-selected-name');
  if (pdfFileInput && fileSelectedName) {
    pdfFileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        fileSelectedName.textContent = `📄 File đã chọn: ${e.target.files[0].name} (${(e.target.files[0].size / 1024 / 1024).toFixed(2)} MB)`;
        fileSelectedName.hidden = false;
      }
    });
  }

  // Teacher Upload Form
  const teacherUploadForm = document.getElementById('teacher-upload-form');
  if (teacherUploadForm) {
    teacherUploadForm.addEventListener('submit', handleTeacherUpload);
  }

  // Student Select Form
  const studentLessonForm = document.getElementById('student-lesson-form');
  if (studentLessonForm) {
    studentLessonForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const selectEl = document.getElementById('student-lesson-select');
      const lessonCode = selectEl ? selectEl.value : '';
      if (!lessonCode) {
        alert("Vui lòng chọn một bài học!");
        return;
      }
      openStudentStudyPack(lessonCode);
    });
  }

  // Quiz Submit Form
  const quizForm = document.getElementById('quiz-form');
  if (quizForm) {
    quizForm.addEventListener('submit', handleQuizSubmit);
  }

  // Socratic Chat Form
  const socraticChatForm = document.getElementById('socratic-chat-form');
  if (socraticChatForm) {
    socraticChatForm.addEventListener('submit', handleSocraticChatSubmit);
  }

  // Feynman Chat Form
  const feynmanChatForm = document.getElementById('feynman-chat-form');
  if (feynmanChatForm) {
    feynmanChatForm.addEventListener('submit', handleFeynmanChatSubmit);
  }

  // Initial Load of Lessons
  loadTeacherLessons();
  loadPublishedLessonsForStudent();
});
