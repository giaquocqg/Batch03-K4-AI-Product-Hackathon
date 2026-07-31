/**
 * 10 mins Study Pack — Frontend Logic for Teacher HITL Workspace & Student Flow.
 * Full integration with Socratic Tutor AI & Feynman Reverse-Role Mode.
 */

let currentLesson = null;
let currentStudentPack = null;
let activeFeynmanSessionId = null;
let activeSocraticSessionId = null;
let currentSearchQuery = null;

const QUICK_PROMPTS_BY_LESSON = {
  "T01": [
    "Mô hình Double Diamond là gì?",
    "Precision vs Recall trong AI?",
    "UX Fallback là gì?",
    "Khung Problem Statement có các yếu tố nào?"
  ],
  "T02": [
    "Vòng lặp ReAct hoạt động thế nào?",
    "Dấu hiệu Agent bị lỗi lặp vô hạn?",
    "Mô hình Lai (Hybrid Pattern) hoạt động thế nào?",
    "Bộ nhớ ngắn hạn vs dài hạn của Agent?"
  ],
  "T03": [
    "specificity beats cleverness là gì?",
    "Lost in the Middle là gì?",
    "Context Bleed là gì?",
    "Bản chất của Tool Calling là gì?"
  ],
  "T04": [
    "5 trụ cột của Responsible AI?",
    "EU AI Act 2024 quy định gì?",
    "Chỉ số North Star metric cho AI?",
    "Tại sao lại nợ rủi ro trong PRD?"
  ]
};

function getTranscriptFilename(lessonCode) {
  if (!lessonCode) return '';
  const match = lessonCode.match(/(\d+)/);
  if (match) {
    const num = match[1].padStart(2, '0');
    return `transcript-${num}-clean.md`;
  }
  return 'transcript-01-clean.md';
}

// --- Tab Switching ---
function switchTab(role) {
  const teacherTab = document.getElementById('tab-teacher');
  const studentTab = document.getElementById('tab-student');
  const teacherView = document.getElementById('teacher-view');
  const studentView = document.getElementById('student-view');

  if (role === 'teacher') {
    if (typeof stopQuizTimer === 'function') stopQuizTimer();
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

// 2. Student Sub-Screen Switcher (4-Screen Flow)
function showStudentScreen(screenId) {
  document.querySelectorAll('.student-sub-screen').forEach(s => {
    s.hidden = s.id !== screenId;
  });
  if (screenId !== 'sp-screen-quiz') {
    stopQuizTimer();
  }
  // Scroll page to top immediately when switching screens
  window.scrollTo(0, 0);
  
  // Reset sticky timer styling
  const timer = document.getElementById('quiz-floating-timer');
  if (timer) {
    timer.classList.remove('is-sticky');
  }
}

// 3. Open Student Study Pack & Move to Screen 2 (Review Room)
async function openStudentStudyPack(lessonCode) {
  const btnOpen = document.getElementById('btn-open-pack');
  if (btnOpen) btnOpen.disabled = true;

  // Reset active Feynman session when switching lessons
  activeFeynmanSessionId = null;
  const feynmanMessages = document.getElementById('feynman-messages-list');
  if (feynmanMessages) feynmanMessages.innerHTML = '';

  try {
    const res = await fetch(`/api/student/lessons/${lessonCode}`);
    const data = await res.json();

    if (!res.ok) {
      alert(`Lỗi: ${data.detail || 'Không tải được bài học.'}`);
      return;
    }

    currentStudentPack = data;
    renderStudentStudyPack(currentStudentPack);
    showStudentScreen('sp-screen-review');

  } catch (err) {
    alert(`Lỗi kết nối: ${err.message}`);
  } finally {
    if (btnOpen) btnOpen.disabled = false;
  }
}

// 4. Render Student Study Pack Components (Review Room)
function renderStudentStudyPack(pack) {
  const titleEl = document.getElementById('sp-review-title');
  const pdfLink = document.getElementById('sp-pdf-link');
  const kwContainer = document.getElementById('sp-keywords-container');
  const summaryEl = document.getElementById('sp-enrich-summary');
  const keyPointsList = document.getElementById('sp-key-points-list');

  if (titleEl) titleEl.textContent = pack.title || pack.lesson_code;

  if (pdfLink) {
    if (pack.pdf_url) {
      pdfLink.href = pack.pdf_url;
      pdfLink.hidden = false;
    } else {
      pdfLink.hidden = true;
    }
  }

  // Render 02 Ý Trọng Tâm
  if (keyPointsList) {
    keyPointsList.innerHTML = '';
    const keyPoints = pack.key_points || [];
    if (keyPoints.length === 0) {
      keyPointsList.innerHTML = '<li style="background: #F8FAFC; border: 2px solid var(--line); border-radius: 18px; padding: 14px 20px;"><p style="font-size: 15px; font-weight: 600;">Xem bài giảng tóm tắt bên dưới để nắm toàn bộ ý chính.</p></li>';
    } else {
      keyPoints.forEach((kpText) => {
        const li = document.createElement('li');
        li.style.cssText = 'background: #F8FAFC; border: 2px solid var(--line); border-radius: 18px; padding: 14px 20px; font-size: 15.5px; font-weight: 600; line-height: 1.5;';
        li.textContent = kpText;
        keyPointsList.appendChild(li);
      });
    }
  }

  // Render 03 Keyword Cần Nhớ
  if (kwContainer) {
    kwContainer.innerHTML = '';
    (pack.keywords || []).forEach(kw => {
      const chip = document.createElement('span');
      chip.style.cssText = 'padding: 8px 16px; border: 2px solid var(--ink); background: var(--clay-pink); font-weight: 700; font-size: 14px; border-radius: 20px; box-shadow: 0px 3px 0px var(--ink);';
      chip.textContent = kw;
      kwContainer.appendChild(chip);
    });
  }

  if (summaryEl) summaryEl.innerHTML = renderMarkdown(pack.enrich_summary || 'Chưa có nội dung tóm tắt.');

  // Hide Feynman Chat container by default on pack load
  const feynmanChatContainer = document.getElementById('feynman-chat-container');
  if (feynmanChatContainer) feynmanChatContainer.hidden = true;

  renderStudentQuickQuiz(pack.questions || []);
}

// 5. Start Virtual Exam (Screen 3)
function startStudentVirtualExam() {
  const quizForm = document.getElementById('quiz-form');
  const quizContainer = document.querySelector('#sp-screen-quiz .card');
  if (quizForm && quizContainer && quizForm.parentElement !== quizContainer) {
    quizContainer.appendChild(quizForm);
  }
  // Reset radios disabled state
  if (quizForm) {
    quizForm.querySelectorAll('input[type="radio"]').forEach(r => {
      r.disabled = false;
      r.checked = false;
    });
  }
  // Reset MCQ card statuses
  const questions = (currentStudentPack && currentStudentPack.questions) ? currentStudentPack.questions : [];
  questions.forEach((q, idx) => {
    const qKey = q.id || idx;
    const card = document.getElementById(`quiz-card-${qKey}`);
    const resultBox = document.getElementById(`quiz-result-${qKey}`);
    if (card) card.className = 'mcq-question-card';
    if (resultBox) resultBox.hidden = true;
  });

  showStudentScreen('sp-screen-quiz');
  startQuizTimer();
}

// 6. 10-Min Virtual Exam Room Timer
let quizTimer = null;
let quizTimeRemaining = 600; // 10 minutes

function startQuizTimer() {
  stopQuizTimer();
  quizTimeRemaining = 600;
  updateQuizTimerDisplay();

  const floatingTimer = document.getElementById('quiz-floating-timer');
  if (floatingTimer) floatingTimer.hidden = false;

  quizTimer = setInterval(() => {
    quizTimeRemaining--;
    updateQuizTimerDisplay();
    if (quizTimeRemaining <= 0) {
      stopQuizTimer();
      alert('Đã hết 10 phút! Hệ thống đang tự động nộp bài làm của bạn.');
      handleQuizSubmit(new Event('submit'));
    }
  }, 1000);
}

function stopQuizTimer() {
  if (quizTimer) {
    clearInterval(quizTimer);
    quizTimer = null;
  }
  const floatingTimer = document.getElementById('quiz-floating-timer');
  if (floatingTimer) floatingTimer.hidden = true;
}

function updateQuizTimerDisplay() {
  const displayEl = document.getElementById('quiz-timer-display');
  if (!displayEl) return;
  const mins = Math.floor(quizTimeRemaining / 60);
  const secs = quizTimeRemaining % 60;
  displayEl.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

// 7. Render Quick Quiz Questions
function renderStudentQuickQuiz(questions) {
  const container = document.getElementById('quiz-questions-container');
  if (!container) return;
  container.innerHTML = '';

  if (questions.length === 0) {
    container.innerHTML = '<p class="text-muted">Chưa có câu hỏi trắc nghiệm nào cho bài học này.</p>';
    return;
  }

  questions.forEach((q, idx) => {
    const card = document.createElement('div');
    card.className = 'mcq-question-card';
    card.id = `quiz-card-${q.id || idx}`;

    const options = q.options || {};
    let optionsHtml = '';

    ['A', 'B', 'C', 'D'].forEach(optKey => {
      if (options[optKey]) {
        optionsHtml += `
          <label class="option-item">
            <input type="radio" name="q_${q.id || idx}" value="${optKey}">
            <span><strong>${optKey}.</strong> ${escapeHtml(options[optKey])}</span>
          </label>
        `;
      }
    });

    card.innerHTML = `
      <div style="font-family: 'Nunito', sans-serif; font-size: 17px; font-weight: 800;">Câu ${idx + 1}: ${escapeHtml(q.question_text)}</div>
      <div class="options-group">
        ${optionsHtml}
      </div>
      <div id="quiz-result-${q.id || idx}" class="quiz-result-box" hidden style="margin-top: 12px; padding: 12px 16px; border: 2px solid var(--ink); border-radius: 16px; font-weight: 600;"></div>
    `;

    container.appendChild(card);
  });
}

// 8. Handle Quiz Submission & Transition to Screen 4 (Results)
function handleQuizSubmit(e) {
  if (e && typeof e.preventDefault === 'function') e.preventDefault();
  stopQuizTimer();
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

    if (card) card.className = `mcq-question-card ${isCorrect ? 'correct' : 'incorrect'}`;

    if (resultBox) {
      if (isCorrect) {
        correctCount++;
        resultBox.style.cssText = 'background: #E8FDF0; border-color: var(--success); color: #166534; margin-top: 12px; padding: 12px 16px; border-radius: 16px; font-weight: 600;';
        resultBox.innerHTML = `
          <strong>✅ Chính xác!</strong>
          <p style="margin-top: 4px;">${escapeHtml(q.explanation || 'Xuất sắc!')}</p>
        `;
      } else {
        resultBox.style.cssText = 'background: #FEF2F2; border-color: var(--error); color: #991B1B; margin-top: 12px; padding: 12px 16px; border-radius: 16px; font-weight: 600;';
        resultBox.innerHTML = `
          <strong>❌ Chưa chính xác!</strong>
          <p style="margin-top: 4px;">Đáp án đúng chính thức: <strong>${q.correct_option}</strong></p>
          <p style="color: var(--muted); margin-top: 4px;">${escapeHtml(q.explanation || '')}</p>
          <button type="button" class="btn btn-sm btn-secondary" style="margin-top: 8px;" onclick="askAiExplainQuestion('${qKey}')">
            🤖 Hỏi AI Giải Thích Thêm ➔
          </button>
        `;
      }
      resultBox.hidden = false;
    }
  });

  // Move quiz form to results container on Screen 4
  const gradedContainer = document.getElementById('graded-quiz-container');
  if (gradedContainer && quizForm) {
    gradedContainer.appendChild(quizForm);
    quizForm.querySelectorAll('input[type="radio"]').forEach(r => r.disabled = true);
  }

  const finalScoreText = document.getElementById('final-score-text');
  const finalScoreFeedback = document.getElementById('final-score-feedback');

  if (finalScoreText) finalScoreText.textContent = `${correctCount}/${questions.length}`;
  if (finalScoreFeedback) {
    if (correctCount >= 8) finalScoreFeedback.textContent = "Xuất sắc! Bạn đã nắm rất vững kiến thức bài học này.";
    else if (correctCount >= 5) finalScoreFeedback.textContent = "Khá tốt! Hãy rà soát lại các câu trả lời sai bên dưới.";
    else finalScoreFeedback.textContent = "Bạn nên đọc lại bài giảng tóm tắt và nhờ AI Socratic giải thích thêm.";
  }

  // Initialize RAG Chatbot for results screen
  initRagChatbotForResults();

  showStudentScreen('sp-screen-results');
}


// =========================================================================
// ==================== CHATBOT 1: AI EXPLAIN ASSISTANT ====================
// =========================================================================

function askAiExplainQuestion(questionId) {
  if (!currentStudentPack || !currentStudentPack.questions) return;
  
  // Find the question by matching ID or fallback to index
  const qIndex = parseInt(questionId, 10);
  const q = currentStudentPack.questions.find((item, idx) => 
    (item.id !== undefined && item.id == questionId) || idx === qIndex
  );
  if (!q) return;

  // Retrieve user's answer choice
  const selectedRadio = document.querySelector(`input[name="q_${questionId}"]:checked`);
  const userChoice = selectedRadio ? selectedRadio.value : 'N/A';

  // Format options
  const options = q.options || {};
  const optA = options.A ? `A. ${options.A}` : '';
  const optB = options.B ? `B. ${options.B}` : '';
  const optC = options.C ? `C. ${options.C}` : '';
  const optD = options.D ? `D. ${options.D}` : '';
  const opts = [optA, optB, optC, optD].filter(Boolean).join(', ');

  // Construct full prompt for LLM (hiển thị cho user và gửi cho LLM)
  const promptText = `Hãy giải thích chi tiết câu hỏi này giúp tôi: "${q.question_text}". Các phương án lựa chọn: ${opts}. Tôi đã chọn phương án ${userChoice}, nhưng đáp án đúng là ${q.correct_option}. Tại sao phương án của tôi chưa đúng và tại sao ${q.correct_option} mới là đáp án chính xác?`;

  const chatbotInput = document.getElementById('chatbot-input');
  const chatbotForm = document.getElementById('chatbot-form');
  const chatbotPanel = document.getElementById('chatbot-panel');

  if (chatbotInput && chatbotForm) {
    chatbotInput.value = promptText;

    // Fix Bug #2: Pin search_query trực tiếp lên form element thay vì dùng biến global
    // để tránh race condition. handleChatbotSubmit sẽ đọc và xóa ngay lập tức.
    chatbotForm.dataset.pendingSearchQuery = q.question_text;

    // Auto-scroll the chatbot panel into view for better UX
    if (chatbotPanel) {
      chatbotPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Dispatch submit event to trigger chatbot submission
    const event = new Event('submit', { cancelable: true });
    chatbotForm.dispatchEvent(event);
  }
}


// =========================================================================
// ================= CHATBOT 2: FEYNMAN REVERSE-ROLE AGENT =================
// =========================================================================

function enterFeynmanMode() {
  if (!currentStudentPack) {
    alert("Vui lòng chọn bài học trước!");
    return;
  }
  showStudentScreen('sp-screen-feynman');
  if (!activeFeynmanSessionId) {
    startFeynmanChat();
  }
}

async function startFeynmanChat() {
  if (!currentStudentPack) {
    alert("Vui lòng chọn bài học trước!");
    return;
  }

  showStudentScreen('sp-screen-feynman');

  const list = document.getElementById('feynman-messages-list');
  const container = document.getElementById('feynman-chat-container');

  if (list) list.innerHTML = '<div class="chat-msg agent"><em>Đang khởi tạo Học sinh AI tò mò...</em></div>';
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
          <div class="chat-msg agent">
            <strong>Học sinh AI (Tò mò):</strong><br>
            ${escapeHtml(data.initial_message).replace(/\n/g, '<br>')}
          </div>
        `;
      }
    } else {
      if (list) list.innerHTML = `<div class="chat-msg agent text-danger">Lỗi: ${data.detail || 'Không thể khởi tạo.'}</div>`;
    }

  } catch (err) {
    if (list) list.innerHTML = `<div class="chat-msg agent text-danger">Lỗi kết nối: ${err.message}</div>`;
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
  userBubble.className = 'chat-msg user';
  userBubble.innerHTML = `<strong>Thầy giáo (Bạn):</strong><br>${escapeHtml(studentAnswer).replace(/\n/g, '<br>')}`;
  if (list) list.appendChild(userBubble);

  if (inputEl) inputEl.value = '';
  if (list) list.scrollTop = list.scrollHeight;

  const aiBubble = document.createElement('div');
  aiBubble.className = 'chat-msg agent';
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

function initRagChatbotForResults() {
  const chatbotMessages = document.getElementById('chatbot-messages');
  const quickChipsContainer = document.getElementById('quick-chips');
  const chatbotForm = document.getElementById('chatbot-form');
  const chatbotInput = document.getElementById('chatbot-input');

  if (chatbotMessages) {
    chatbotMessages.innerHTML = `
      <div class="chat-message system">
        <p>Chào bạn! Tôi là trợ lý RAG. Hãy hỏi tôi về bài giảng này. Tất cả câu trả lời của tôi đều có trích dẫn mã đoạn <code>[Txx-NNN]</code> để bạn kiểm chứng.</p>
      </div>
    `;
  }

  if (quickChipsContainer && currentStudentPack) {
    quickChipsContainer.innerHTML = '';
    const transcriptFile = getTranscriptFilename(currentStudentPack.lesson_code);
    let transcriptId = 'T01';
    const match = transcriptFile.match(/transcript-(\d+)-clean/);
    if (match) {
      transcriptId = `T${match[1]}`;
    }

    const chips = QUICK_PROMPTS_BY_LESSON[transcriptId] || ["Tóm tắt bài học này", "Hãy cho tôi biết trọng tâm bài giảng"];
    chips.forEach((promptText) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'quick-chip';
      chip.textContent = promptText;
      chip.addEventListener('click', () => {
        if (chatbotInput) {
          chatbotInput.value = promptText;
        }
        if (chatbotForm) {
          const event = new Event('submit', { cancelable: true });
          chatbotForm.dispatchEvent(event);
        }
      });
      quickChipsContainer.append(chip);
    });
  }
}

async function handleChatbotSubmit(event) {
  event.preventDefault();
  if (!currentStudentPack) return;

  // Fix Bug #2: Ưu tiên đọc pendingSearchQuery từ form element (set bởi askAiExplainQuestion)
  // Fallback về biến global currentSearchQuery (set bởi các flow khác)
  const chatbotFormEl = document.getElementById('chatbot-form');
  const searchQueryToSend =
    (chatbotFormEl && chatbotFormEl.dataset.pendingSearchQuery)
      ? chatbotFormEl.dataset.pendingSearchQuery
      : currentSearchQuery;
  if (chatbotFormEl) delete chatbotFormEl.dataset.pendingSearchQuery; // xóa ngay sau khi đọc
  currentSearchQuery = null; // reset biến global

  const chatbotInput = document.getElementById('chatbot-input');
  const chatbotMessages = document.getElementById('chatbot-messages');
  const question = chatbotInput ? chatbotInput.value.trim() : '';
  if (!question) return;

  // Append user message
  const userMsg = document.createElement('div');
  userMsg.className = 'chat-message user';
  userMsg.innerHTML = `<p>${escapeHtml(question)}</p>`;
  if (chatbotMessages) {
    chatbotMessages.append(userMsg);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }

  if (chatbotInput) {
    chatbotInput.value = '';
    chatbotInput.disabled = true;
  }

  // Append typing indicator
  const typingMsg = document.createElement('div');
  typingMsg.className = 'chat-message assistant typing';
  typingMsg.innerHTML = `<p>Trợ lý đang truy xuất bài giảng...</p>`;
  if (chatbotMessages) {
    chatbotMessages.append(typingMsg);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }

  const transcriptFile = getTranscriptFilename(currentStudentPack.lesson_code);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transcript: transcriptFile,
        question: question,
        search_query: searchQueryToSend
      })
    });

    const payload = await response.json();
    typingMsg.remove();

    if (response.status === 429) {
      const errorMsg = document.createElement('div');
      errorMsg.className = 'chat-message system';
      errorMsg.style.borderColor = 'var(--error)';
      errorMsg.innerHTML = `<p>⚠️ ${payload.detail || 'Hỏi quá nhanh. Hãy thử lại sau.'}</p>`;
      if (chatbotMessages) chatbotMessages.append(errorMsg);
    } else if (!response.ok) {
      const errorMsg = document.createElement('div');
      errorMsg.className = 'chat-message system';
      errorMsg.style.borderColor = 'var(--error)';
      errorMsg.innerHTML = `<p>⚠️ ${payload.detail || 'Lỗi xử lý câu hỏi.'}</p>`;
      if (chatbotMessages) chatbotMessages.append(errorMsg);
    } else {
      const assistantMsg = document.createElement('div');
      assistantMsg.className = 'chat-message assistant';
      assistantMsg.append(formatAssistantResponseText(payload.answer));
      if (chatbotMessages) chatbotMessages.append(assistantMsg);
    }
  } catch (error) {
    typingMsg.remove();
    const errorMsg = document.createElement('div');
    errorMsg.className = 'chat-message system';
    errorMsg.innerHTML = `<p>⚠️ Lỗi kết nối mạng: ${error.message}</p>`;
    if (chatbotMessages) chatbotMessages.append(errorMsg);
  } finally {
    if (chatbotInput) {
      chatbotInput.disabled = false;
      chatbotInput.focus();
    }
    if (chatbotMessages) chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }
}

function formatAssistantResponseText(text) {
  const container = document.createElement('div');
  const regex = /\[(T\d{2}-\d{3})\]/g;
  
  let lastIndex = 0;
  let match;
  
  const p = document.createElement('p');
  
  while ((match = regex.exec(text)) !== null) {
    const code = match[1];
    const textBefore = text.slice(lastIndex, match.index);
    if (textBefore) {
      p.append(document.createTextNode(textBefore));
    }
    p.append(citationButton(code));
    lastIndex = regex.lastIndex;
  }
  
  const textAfter = text.slice(lastIndex);
  if (textAfter) {
    p.append(document.createTextNode(textAfter));
  }
  
  container.append(p);
  return container;
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
    if (!currentStudentPack) return;
    const transcriptFile = getTranscriptFilename(currentStudentPack.lesson_code);
    const params = new URLSearchParams({ transcript: transcriptFile, code });
    const response = await fetch(`/api/citation?${params}`);
    const payload = await response.json();
    if (!response.ok) {
      alert(payload.error || 'Không tìm thấy đoạn trích nguồn.');
      return;
    }
    const citationCode = document.querySelector('#citation-code');
    const citationText = document.querySelector('#citation-text');
    const citationWarning = document.querySelector('#citation-warning');
    const citationDialog = document.querySelector('#citation-dialog');
    
    if (citationCode) citationCode.textContent = `[${payload.code}]`;
    if (citationText) citationText.textContent = payload.text;
    if (citationWarning) citationWarning.hidden = !payload.has_unclear;
    if (citationDialog) citationDialog.showModal();
  } catch (error) {
    alert('Không mở được citation: ' + error.message);
  }
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

  // Start Student Quiz Button listener
  const startStudentQuizBtn = document.getElementById('btn-start-student-quiz');
  if (startStudentQuizBtn) {
    startStudentQuizBtn.addEventListener('click', startStudentVirtualExam);
  }

  // Start Feynman Button listener
  const startFeynmanBtn = document.getElementById('btn-start-feynman');
  if (startFeynmanBtn) {
    startFeynmanBtn.addEventListener('click', startFeynmanChat);
  }



  // Feynman Chat Form
  const feynmanChatForm = document.getElementById('feynman-chat-form');
  if (feynmanChatForm) {
    feynmanChatForm.addEventListener('submit', handleFeynmanChatSubmit);
  }

  // RAG Chatbot Form
  const chatbotForm = document.getElementById('chatbot-form');
  if (chatbotForm) {
    chatbotForm.addEventListener('submit', handleChatbotSubmit);
  }

  // Scroll listener to make timer sticky when static header is out of view
  window.addEventListener('scroll', () => {
    const timer = document.getElementById('quiz-floating-timer');
    if (!timer || timer.hidden) return;

    const header = document.querySelector('.quiz-header-static');
    if (header) {
      const rect = header.getBoundingClientRect();
      if (rect.bottom < 0) {
        timer.classList.add('is-sticky');
      } else {
        timer.classList.remove('is-sticky');
      }
    }
  });

  // Close citation dialog
  const closeDialog = document.getElementById('close-dialog');
  if (closeDialog) {
    closeDialog.addEventListener('click', () => {
      const dialog = document.getElementById('citation-dialog');
      if (dialog) dialog.close();
    });
  }

  // Close citation dialog when clicking backdrop
  const citationDialog = document.getElementById('citation-dialog');
  if (citationDialog) {
    citationDialog.addEventListener('click', (event) => {
      const rect = citationDialog.getBoundingClientRect();
      const isInDialog = (
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width
      );
      if (!isInDialog) {
        citationDialog.close();
      }
    });
  }

  // Initial Load of Lessons
  loadTeacherLessons();
  loadPublishedLessonsForStudent();
});
