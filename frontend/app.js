// ============================================================
// Shared settings
// ============================================================
const API_BASE = "http://127.0.0.1:8000";
const STUDENT_ID = 1; // seeded demo student (no login in this version)

// ============================================================
// Helpers
// ============================================================
async function apiFetch(path, options = {}) {
  let response;
  try {
    response = await fetch(API_BASE + path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (error) {
    throw new Error("Cannot reach the server. Please check that the backend is running.");
  }

  let data = null;
  try {
    data = await response.json();
  } catch (error) {
    // response had no JSON body
  }

  if (!response.ok) {
    let message = "Something went wrong. Please try again.";
    if (data && typeof data.detail === "string") {
      message = data.detail;
    } else if (data && Array.isArray(data.detail)) {
      message = "Invalid input. Please check what you typed.";
    }
    throw new Error(message);
  }
  return data;
}

// type: "info" | "success" | "error"
function showMessage(container, text, type) {
  container.textContent = "";
  if (!text) return;
  const box = document.createElement("div");
  box.className = "msg " + type;
  box.textContent = text; // textContent (not innerHTML) keeps it safe from injected HTML
  container.appendChild(box);
}

function makeCell(text) {
  const td = document.createElement("td");
  td.textContent = text;
  return td;
}

// ============================================================
// Home page
// ============================================================
async function initHome() {
  const status = document.getElementById("status");
  try {
    const data = await apiFetch("/");
    status.className = "msg success";
    status.textContent = "Backend status: " + data.message;
  } catch (error) {
    status.className = "msg error";
    status.textContent = error.message;
  }
}

// ============================================================
// Question list page
// ============================================================
async function loadQuestions() {
  const message = document.getElementById("message");
  const tbody = document.getElementById("question-rows");
  const category = document.getElementById("category").value;
  const difficulty = document.getElementById("difficulty").value;

  const params = new URLSearchParams();
  if (category) params.append("category", category);
  if (difficulty) params.append("difficulty", difficulty);
  const query = params.toString() ? "?" + params.toString() : "";

  tbody.textContent = "";
  showMessage(message, "Loading questions...", "info");

  try {
    const questions = await apiFetch("/questions" + query);
    if (questions.length === 0) {
      showMessage(message, "No questions found for this filter.", "info");
      return;
    }
    showMessage(message, "", "info");

    questions.forEach((q) => {
      const tr = document.createElement("tr");
      tr.appendChild(makeCell(q.question_id));

      const titleCell = document.createElement("td");
      const link = document.createElement("a");
      link.href = "question.html?id=" + encodeURIComponent(q.question_id);
      link.textContent = q.title;
      titleCell.appendChild(link);
      tr.appendChild(titleCell);

      tr.appendChild(makeCell(q.category));
      tr.appendChild(makeCell(q.difficulty || "-"));
      tbody.appendChild(tr);
    });
  } catch (error) {
    showMessage(message, error.message, "error");
  }
}

function initQuestions() {
  document.getElementById("category").addEventListener("change", loadQuestions);
  document.getElementById("difficulty").addEventListener("change", loadQuestions);
  loadQuestions();
}

// ============================================================
// Question detail page
// ============================================================
async function initQuestion() {
  const message = document.getElementById("message");
  const id = new URLSearchParams(window.location.search).get("id");

  if (!id || !/^\d+$/.test(id)) {
    showMessage(message, "No question selected. Please go back and choose a question.", "error");
    return;
  }

  showMessage(message, "Loading question...", "info");
  let question;
  try {
    question = await apiFetch("/questions/" + id);
  } catch (error) {
    showMessage(message, error.message, "error");
    return;
  }
  showMessage(message, "", "info");

  document.getElementById("q-title").textContent = question.title;
  document.getElementById("q-category").textContent = question.category;
  document.getElementById("q-difficulty").textContent = question.difficulty || "";
  document.getElementById("q-description").textContent = question.description;
  document.getElementById("q-input").textContent = question.sample_input || "-";
  document.getElementById("q-output").textContent = question.expected_output || "-";
  document.getElementById("question-card").hidden = false;
  document.getElementById("answer-card").hidden = false;

  const result = document.getElementById("result");
  const answerBox = document.getElementById("answer");
  const submitBtn = document.getElementById("submit-btn");
  const completeBtn = document.getElementById("complete-btn");

  async function sendAttempt(markCompleted) {
    const answer = answerBox.value.trim();
    if (!markCompleted && answer === "") {
      showMessage(result, "Please type an answer before submitting.", "error");
      return;
    }

    submitBtn.disabled = true;
    completeBtn.disabled = true;
    showMessage(result, "Saving...", "info");

    try {
      const data = await apiFetch("/attempts", {
        method: "POST",
        body: JSON.stringify({
          student_id: STUDENT_ID,
          question_id: Number(id),
          submitted_answer: answer || null,
          mark_completed: markCompleted,
        }),
      });
      showMessage(
        result,
        data.message + " Score: " + data.score + "/100",
        data.completed ? "success" : "info"
      );
    } catch (error) {
      showMessage(result, error.message, "error");
    } finally {
      submitBtn.disabled = false;
      completeBtn.disabled = false;
    }
  }

  submitBtn.addEventListener("click", () => sendAttempt(false));
  completeBtn.addEventListener("click", () => sendAttempt(true));
}

// ============================================================
// Progress page
// ============================================================
async function initProgress() {
  const message = document.getElementById("message");
  showMessage(message, "Loading progress...", "info");

  try {
    const p = await apiFetch("/students/" + STUDENT_ID + "/progress");
    showMessage(message, "", "info");

    document.getElementById("student-name").textContent = "Student: " + p.student_name;
    document.getElementById("s-attempted").textContent =
      p.questions_attempted + " / " + p.total_questions;
    document.getElementById("s-completed").textContent = p.questions_completed;
    document.getElementById("s-average").textContent = p.average_score;
    document.getElementById("s-attempts").textContent = p.total_attempts;
    document.getElementById("stats").hidden = false;

    if (p.recent_attempts.length === 0) {
      showMessage(message, "No attempts yet. Open a question and submit your first answer!", "info");
      return;
    }

    const tbody = document.getElementById("attempt-rows");
    tbody.textContent = "";
    p.recent_attempts.forEach((a) => {
      const tr = document.createElement("tr");
      tr.appendChild(makeCell(a.title));
      tr.appendChild(makeCell(a.score));
      tr.appendChild(makeCell(a.completed ? "Yes" : "No"));
      tr.appendChild(makeCell(new Date(a.attempted_at).toLocaleString()));
      tbody.appendChild(tr);
    });
    document.getElementById("history-card").hidden = false;
  } catch (error) {
    showMessage(message, error.message, "error");
  }
}

// ============================================================
// Chatbot page
// ============================================================
function initChatbot() {
  const box = document.getElementById("chat-box");
  const input = document.getElementById("chat-input");
  const sendBtn = document.getElementById("send-btn");
  const message = document.getElementById("message");

  function addBubble(text, who) {
    const div = document.createElement("div");
    div.className = "bubble " + who;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
  }

  addBubble("Hi! Ask me about Python, REST APIs, FastAPI, MySQL or interview preparation. Type 'help' to see examples.", "bot");

  async function send() {
    const text = input.value.trim();
    if (text === "") {
      showMessage(message, "Please type a message first.", "error");
      return;
    }
    showMessage(message, "", "info");
    addBubble(text, "user");
    input.value = "";
    sendBtn.disabled = true;

    try {
      const data = await apiFetch("/chat", {
        method: "POST",
        body: JSON.stringify({ message: text }),
      });
      addBubble(data.reply, "bot");
    } catch (error) {
      showMessage(message, error.message, "error");
    } finally {
      sendBtn.disabled = false;
      input.focus();
    }
  }

  sendBtn.addEventListener("click", send);
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") send();
  });
}

// ============================================================
// Start the right code for the current page
// ============================================================
document.addEventListener("DOMContentLoaded", () => {
  const page = document.body.dataset.page;
  if (page === "home") initHome();
  if (page === "questions") initQuestions();
  if (page === "question") initQuestion();
  if (page === "progress") initProgress();
  if (page === "chatbot") initChatbot();
});
