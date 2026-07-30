const generateForm = document.querySelector('#generate-form');
const transcriptSelect = document.querySelector('#transcript-select');
const statusPanel = document.querySelector('#status-panel');
const keyPointsList = document.querySelector('#key-points');
const keywordsContainer = document.querySelector('#keywords');
const quizForm = document.querySelector('#quiz-form');
const quizQuestionsList = document.querySelector('#quiz-questions-list');
const scoreSection = document.querySelector('#score-section');
const scoreText = document.querySelector('#score-text');
const scoreFeedbackText = document.querySelector('#score-feedback-text');
const weakAreasCard = document.querySelector('#weak-areas-card');
const weakCitationsList = document.querySelector('#weak-citations-list');
const chatbotPanel = document.querySelector('#chatbot-panel');
const chatbotMessages = document.querySelector('#chatbot-messages');
const chatbotForm = document.querySelector('#chatbot-form');
const chatbotInput = document.querySelector('#chatbot-input');
const quickChipsContainer = document.querySelector('#quick-chips');

const citationDialog = document.querySelector('#citation-dialog');
const citationCode = document.querySelector('#citation-code');
const citationText = document.querySelector('#citation-text');
const citationWarning = document.querySelector('#citation-warning');

const startQuizBtn = document.querySelector('#start-quiz-btn');

let activeTranscript = '';
let currentQuestionsData = [];
let examTimer = null;
let examTimeRemaining = 600; // 10 minutes (in seconds)

// Quick suggestions for RAG chatbot
const QUICK_PROMPTS_BY_LESSON = {
  "T10": [
    "Self-Attention là gì?",
    "Emergent Capabilities là gì?",
    "Phân biệt SFT vs RLHF/DPO",
    "Tại sao tiếng Việt tốn nhiều token?"
  ],
  "T11": [
    "Self-Attention là gì?",
    "Emergent Capabilities là gì?",
    "Phân biệt SFT vs RLHF/DPO",
    "Tại sao tiếng Việt tốn nhiều token?"
  ],
  "T12": [
    "Mô hình Double Diamond là gì?",
    "Precision vs Recall trong AI?",
    "UX Fallback là gì?",
    "Khung Problem Statement có các yếu tố nào?"
  ],
  "T13": [
    "Vòng lặp ReAct hoạt động thế nào?",
    "Dấu hiệu Agent bị lỗi lặp vô hạn?",
    "Mô hình Lai (Hybrid Pattern) hoạt động thế nào?",
    "Bộ nhớ ngắn hạn vs dài hạn của Agent?"
  ],
  "T14": [
    "specificity beats cleverness là gì?",
    "Lost in the Middle là gì?",
    "Context Bleed là gì?",
    "Bản chất của Tool Calling là gì?"
  ],
  "T15": [
    "5 trụ cột của Responsible AI?",
    "EU AI Act 2024 quy định gì?",
    "Chỉ số North Star metric cho AI?",
    "Tại sao lại nợ rủi ro trong PRD?"
  ]
};

// Screen navigation controller
function showScreen(screenId) {
  document.querySelectorAll('.view-screen').forEach((screen) => {
    screen.hidden = screen.id !== screenId;
  });
  const timerBox = document.querySelector('#quiz-timer-box');
  if (timerBox) {
    timerBox.classList.remove('is-sticky');
  }
  window.scrollTo(0, 0);
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
      alert(payload.error || 'Không tìm thấy đoạn trích nguồn.');
      return;
    }
    citationCode.textContent = `[${payload.code}]`;
    citationText.textContent = payload.text;
    citationWarning.hidden = !payload.has_unclear;
    citationDialog.showModal();
  } catch (error) {
    alert('Không mở được citation: ' + error.message);
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

// Load Study Pack and populate Screen 2 review elements
async function handleLoadStudyPack(event) {
  event.preventDefault();
  const selectedFile = transcriptSelect.value;
  if (!selectedFile) return;

  // Clear any active timers
  if (examTimer) {
    clearInterval(examTimer);
    examTimer = null;
  }

  setStatus('loading', 'Đang tải dữ liệu Study Pack từ Database...', 'Lấy tóm tắt và bộ câu hỏi đã qua kiểm duyệt.');

  try {
    const params = new URLSearchParams({ transcript: selectedFile });
    const response = await fetch(`/api/study-pack?${params}`);
    const payload = await response.json();
    
    if (!response.ok) {
      setStatus('error', 'Không tải được Study Pack', payload.error || 'Lỗi server.');
      return;
    }

    activeTranscript = selectedFile;
    const transcriptId = payload.transcript.transcript_id;
    
    // Render Key Points
    keyPointsList.innerHTML = '';
    payload.study_pack.key_points.forEach((item) => {
      const li = document.createElement('li');
      const p = document.createElement('p');
      p.textContent = item.content;
      const cites = document.createElement('div');
      cites.className = 'citation-list';
      item.citations.forEach((code) => cites.append(citationButton(code)));
      li.append(p, cites);
      keyPointsList.append(li);
    });

    // Render Keywords
    keywordsContainer.innerHTML = '';
    payload.study_pack.keywords.forEach((keyword) => {
      const span = document.createElement('span');
      span.textContent = keyword;
      keywordsContainer.append(span);
    });

    // Reset Quiz Form Container structure
    const gradedQuizContainer = document.querySelector('#graded-quiz-container');
    const quizContainerFull = document.querySelector('.quiz-container-full');
    if (quizForm.parentElement === gradedQuizContainer) {
      quizContainerFull.appendChild(quizForm);
    }

    // Render Questions (MCQ) - Options are hidden and un-evaluated initially
    quizQuestionsList.innerHTML = '';
    currentQuestionsData = payload.study_pack.questions;
    
    currentQuestionsData.forEach((q, index) => {
      const qNum = String(index + 1).padStart(2, '0');
      const questionCard = document.createElement('article');
      questionCard.className = 'question-mcq-card';
      questionCard.id = `q-card-${index}`;
      
      const qHeader = document.createElement('div');
      qHeader.className = 'q-header';
      qHeader.innerHTML = `<span class="q-number">${qNum}</span><h4 class="q-text">${q.question}</h4>`;
      questionCard.append(qHeader);
      
      const optionsList = document.createElement('div');
      optionsList.className = 'options-list';
      
      q.options.forEach((opt) => {
        const optionVal = opt.charAt(0); // Option letter A, B, C, D
        const label = document.createElement('label');
        label.className = 'option-label';
        label.dataset.option = optionVal;
        
        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = `question-${index}`;
        radio.value = optionVal;
        
        const textSpan = document.createElement('span');
        textSpan.className = 'option-text';
        textSpan.textContent = opt;
        
        label.append(radio, textSpan);
        optionsList.append(label);
        
        radio.addEventListener('change', () => {
          optionsList.querySelectorAll('.option-label').forEach(lbl => lbl.classList.remove('selected'));
          if (radio.checked) {
            label.classList.add('selected');
          }
        });
      });
      
      questionCard.append(optionsList);
      
      const feedbackArea = document.createElement('div');
      feedbackArea.className = 'q-feedback-area';
      feedbackArea.hidden = true;
      feedbackArea.innerHTML = `
        <div class="q-correct-status"></div>
        <p class="q-explanation"></p>
        <div class="q-citations citation-list"></div>
      `;
      questionCard.append(feedbackArea);
      
      quizQuestionsList.append(questionCard);
    });

    // Reset Chatbot Messages
    chatbotMessages.innerHTML = `
      <div class="chat-message system">
        <p>Chào bạn! Tôi là trợ lý RAG. Hãy hỏi tôi về bài giảng này. Tất cả câu trả lời của tôi đều có trích dẫn mã đoạn <code>[Txx-NNN]</code> để bạn kiểm chứng.</p>
      </div>
    `;
    
    // Render Quick Prompts chips
    quickChipsContainer.innerHTML = '';
    const chips = QUICK_PROMPTS_BY_LESSON[transcriptId] || ["Tóm tắt bài học này", "Hãy cho tôi biết trọng tâm bài giảng"];
    chips.forEach((promptText) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'quick-chip';
      chip.textContent = promptText;
      chip.addEventListener('click', () => {
        chatbotInput.value = promptText;
        chatbotForm.requestSubmit();
      });
      quickChipsContainer.append(chip);
    });

    // Setup submit button state
    const submitBtn = document.querySelector('#submit-quiz-btn');
    submitBtn.style.display = 'flex';
    submitBtn.disabled = false;
    submitBtn.querySelector('span').textContent = 'Nộp bài & Chấm điểm';

    statusPanel.hidden = true;
    showScreen('screen-review');

  } catch (error) {
    setStatus('error', 'Lỗi kết nối hoặc xử lý', error.message);
  }
}

// Start Countdown Timer and transition to Screen 3 (Virtual Exam Room)
function handleStartQuiz() {
  // Move quizForm back to Screen 3 if it was previously moved to Screen 4
  const gradedQuizContainer = document.querySelector('#graded-quiz-container');
  const quizContainerFull = document.querySelector('.quiz-container-full');
  if (quizForm.parentElement === gradedQuizContainer) {
    quizContainerFull.appendChild(quizForm);
  }

  // Reset quiz form inputs & selected styles
  quizForm.querySelectorAll('input[type="radio"]').forEach(radio => {
    radio.disabled = false;
    radio.checked = false;
  });
  quizForm.querySelectorAll('.option-label').forEach(label => {
    label.classList.remove('selected', 'is-correct-option', 'is-wrong-selection');
  });
  
  // Hide feedback areas & reset card border status
  quizForm.querySelectorAll('.question-mcq-card').forEach(card => {
    card.classList.remove('correct', 'incorrect');
    const feedbackArea = card.querySelector('.q-feedback-area');
    if (feedbackArea) feedbackArea.hidden = true;
  });

  // Restore submit button state
  const submitBtn = document.querySelector('#submit-quiz-btn');
  if (submitBtn) {
    submitBtn.style.display = 'flex';
    submitBtn.disabled = false;
    submitBtn.querySelector('span').textContent = 'Nộp bài & Chấm điểm';
  }

  showScreen('screen-quiz');
  
  examTimeRemaining = 600; // 10 minutes
  updateTimerDisplay();
  
  if (examTimer) clearInterval(examTimer);
  examTimer = setInterval(() => {
    examTimeRemaining--;
    updateTimerDisplay();
    if (examTimeRemaining <= 0) {
      clearInterval(examTimer);
      examTimer = null;
      alert('Đã hết 10 phút! Hệ thống đang tự động nộp bài làm của bạn.');
      submitQuizData(true);
    }
  }, 1000);
}

function updateTimerDisplay() {
  const timerElement = document.querySelector('#quiz-timer');
  if (!timerElement) return;

  const minutes = Math.floor(examTimeRemaining / 60);
  const seconds = examTimeRemaining % 60;
  timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  
  const timerBox = document.querySelector('.timer-box-clay');
  if (timerBox) {
    if (examTimeRemaining <= 60) {
      timerBox.style.background = 'var(--error)';
      timerBox.style.color = 'var(--white)';
    } else if (examTimeRemaining <= 180) {
      timerBox.style.background = 'var(--warning)';
      timerBox.style.color = 'var(--ink)';
    } else {
      timerBox.style.background = 'var(--clay-mint)';
      timerBox.style.color = 'var(--ink)';
    }
  }
}

// Core grading submit logic
async function submitQuizData(isAutoSubmit = false) {
  // Clear countdown interval
  if (examTimer) {
    clearInterval(examTimer);
    examTimer = null;
  }

  // Gather answers
  const answers = [];
  let unansweredCount = 0;
  
  currentQuestionsData.forEach((_, index) => {
    const selectedRadio = quizForm.querySelector(`input[name="question-${index}"]:checked`);
    if (selectedRadio) {
      answers.push(selectedRadio.value);
    } else {
      answers.push('');
      unansweredCount++;
    }
  });

  if (!isAutoSubmit && unansweredCount > 0) {
    alert(`Vui lòng hoàn thành tất cả câu hỏi trước khi nộp bài! (Còn ${unansweredCount} câu chưa làm)`);
    // Restart timer
    handleStartQuiz();
    return;
  }

  const submitBtn = document.querySelector('#submit-quiz-btn');
  submitBtn.disabled = true;
  submitBtn.querySelector('span').textContent = 'Đang chấm điểm...';

  try {
    const response = await fetch('/api/quiz/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transcript: activeTranscript,
        answers: answers
      })
    });
    
    const payload = await response.json();
    if (!response.ok) {
      alert(payload.error || 'Gặp lỗi khi chấm điểm.');
      return;
    }

    // Display grade card score
    scoreText.textContent = `${payload.score}/10`;
    if (payload.score >= 8) {
      scoreFeedbackText.textContent = "Xuất sắc! Bạn đã nắm vững trọng tâm bài giảng.";
    } else if (payload.score >= 5) {
      scoreFeedbackText.textContent = "Tốt, nhưng bạn vẫn còn một vài lỗ hổng kiến thức cần củng cố thêm.";
    } else {
      scoreFeedbackText.textContent = "Bạn cần rà soát lại tài liệu bài giảng này kỹ hơn.";
    }
    scoreSection.hidden = false;

    // Display weak areas citations
    if (payload.weak_citations && payload.weak_citations.length > 0) {
      weakCitationsList.innerHTML = '';
      payload.weak_citations.forEach((code) => {
        weakCitationsList.append(citationButton(code));
      });
      weakAreasCard.hidden = false;
    } else {
      weakAreasCard.hidden = true;
    }

    // Unveil detailed feedback for each question card
    payload.results.forEach((res, index) => {
      const card = document.querySelector(`#q-card-${index}`);
      card.classList.remove('correct', 'incorrect');
      card.classList.add(res.is_correct ? 'correct' : 'incorrect');
      
      const feedbackArea = card.querySelector('.q-feedback-area');
      feedbackArea.hidden = false;
      
      const statusDiv = feedbackArea.querySelector('.q-correct-status');
      statusDiv.textContent = res.is_correct ? '✓ ĐÚNG' : '✗ SAI';
      
      const expP = feedbackArea.querySelector('.q-explanation');
      expP.textContent = res.explanation;
      
      const citesDiv = feedbackArea.querySelector('.q-citations');
      citesDiv.innerHTML = '';
      res.citations.forEach((code) => citesDiv.append(citationButton(code)));
      
      // Paint feedback styles on options labels
      const optionsLabels = card.querySelectorAll('.option-label');
      optionsLabels.forEach((label) => {
        label.classList.remove('is-correct-option', 'is-wrong-selection');
        const optVal = label.dataset.option;
        
        if (optVal === res.correct_option) {
          label.classList.add('is-correct-option');
        }
        if (optVal === res.user_answer && !res.is_correct) {
          label.classList.add('is-wrong-selection');
        }
      });
    });

    // Move quiz form inside results panel left side
    document.querySelector('#graded-quiz-container').appendChild(quizForm);
    
    // Disable inputs so student can no longer alter options
    quizForm.querySelectorAll('input[type="radio"]').forEach(radio => radio.disabled = true);
    
    // Hide submit button in the graded view
    submitBtn.style.display = 'none';

    // Show Screen 4: Results & RAG Assistant
    showScreen('screen-results');
    chatbotPanel.hidden = false;
    
    // Smooth scroll to score feedback
    scoreSection.scrollIntoView({ behavior: 'smooth', block: 'center' });

  } catch (error) {
    alert('Lỗi kết nối khi nộp bài: ' + error.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.querySelector('span').textContent = 'Nộp bài & Chấm điểm';
  }
}

async function handleChatbotSubmit(event) {
  event.preventDefault();
  const question = chatbotInput.value.trim();
  if (!question) return;

  // Append user message
  const userMsg = document.createElement('div');
  userMsg.className = 'chat-message user';
  userMsg.innerHTML = `<p>${question}</p>`;
  chatbotMessages.append(userMsg);
  chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

  chatbotInput.value = '';
  chatbotInput.disabled = true;

  // Append assistant typing indicator bubble
  const typingMsg = document.createElement('div');
  typingMsg.className = 'chat-message assistant typing';
  typingMsg.innerHTML = `<p>Trợ lý đang truy xuất bài giảng...</p>`;
  chatbotMessages.append(typingMsg);
  chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        transcript: activeTranscript,
        question: question
      })
    });

    const payload = await response.json();
    typingMsg.remove();

    if (response.status === 429) {
      const errorMsg = document.createElement('div');
      errorMsg.className = 'chat-message system';
      errorMsg.style.borderColor = 'var(--error)';
      errorMsg.innerHTML = `<p>⚠️ ${payload.error || 'Hỏi quá nhanh. Hãy thử lại sau.'}</p>`;
      chatbotMessages.append(errorMsg);
    } else if (!response.ok) {
      const errorMsg = document.createElement('div');
      errorMsg.className = 'chat-message system';
      errorMsg.style.borderColor = 'var(--error)';
      errorMsg.innerHTML = `<p>⚠️ ${payload.error || 'Lỗi xử lý câu hỏi.'}</p>`;
      chatbotMessages.append(errorMsg);
    } else {
      const assistantMsg = document.createElement('div');
      assistantMsg.className = 'chat-message assistant';
      assistantMsg.append(formatAssistantResponseText(payload.answer));
      chatbotMessages.append(assistantMsg);
    }

  } catch (error) {
    typingMsg.remove();
    const errorMsg = document.createElement('div');
    errorMsg.className = 'chat-message system';
    errorMsg.innerHTML = `<p>⚠️ Lỗi kết nối mạng: ${error.message}</p>`;
    chatbotMessages.append(errorMsg);
  } finally {
    chatbotInput.disabled = false;
    chatbotInput.focus();
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
  }
}

// Load available transcripts from active corpus at starting
async function loadTranscripts() {
  try {
    const response = await fetch('/api/transcripts');
    const payload = await response.json();
    transcriptSelect.innerHTML = '<option value="">Chọn bài giảng để ôn tập</option>';
    payload.transcripts.forEach((transcript) => {
      const option = document.createElement('option');
      option.value = transcript.file_name;
      option.textContent = `${transcript.transcript_id} · ${transcript.title.replace('Transcript bài giảng (bản sạch) — ', '').replace('Study Pack corpus - ', '')}`;
      transcriptSelect.append(option);
    });
  } catch (error) {
    transcriptSelect.innerHTML = '<option value="">Không tải được danh sách</option>';
    setStatus('error', 'Không tải được active corpus', error.message);
  }
}

// Attach event listeners
generateForm.addEventListener('submit', handleLoadStudyPack);
startQuizBtn.addEventListener('click', handleStartQuiz);
quizForm.addEventListener('submit', (e) => {
  e.preventDefault();
  submitQuizData(false);
});
chatbotForm.addEventListener('submit', handleChatbotSubmit);
document.querySelector('#close-dialog').addEventListener('click', () => citationDialog.close());

// Close citation modal when clicking backdrop
citationDialog.addEventListener('click', (event) => {
  const rect = citationDialog.getBoundingClientRect();
  const isInDialog = (rect.top <= event.clientY && event.clientY <= rect.top + rect.height &&
                      rect.left <= event.clientX && event.clientX <= rect.left + rect.width);
  if (!isInDialog) {
    citationDialog.close();
  }
});

// Setup back buttons navigation
document.querySelectorAll('.back-to-setup-btn').forEach((btn) => {
  btn.addEventListener('click', () => {
    // Clear timer if navigating back
    if (examTimer) {
      clearInterval(examTimer);
      examTimer = null;
    }
    showScreen('screen-setup');
  });
});

document.querySelector('#review-again-btn').addEventListener('click', () => {
  showScreen('screen-review');
});

// Toggle sticky timer on scroll
window.addEventListener('scroll', () => {
  const quizScreen = document.querySelector('#screen-quiz');
  if (quizScreen && !quizScreen.hidden) {
    const timerBox = document.querySelector('#quiz-timer-box');
    const header = document.querySelector('.quiz-header-static');
    if (timerBox && header) {
      const headerRect = header.getBoundingClientRect();
      // If the header starts leaving the viewport, make the timer box sticky
      if (headerRect.bottom < 20) {
        timerBox.classList.add('is-sticky');
      } else {
        timerBox.classList.remove('is-sticky');
      }
    }
  }
});

loadTranscripts();
showScreen('screen-setup');
