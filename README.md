# Smart Placement Preparation Assistant

## Project Objective
A web application that helps engineering students prepare for technical placement interviews. Students can browse Python practice questions, submit answers, track their progress, and ask a rule-based chatbot basic questions about Python, REST APIs, FastAPI and MySQL.

## Team Members
| Name | ID | Role |
|------|----|------|
|      |    |      |

College / Department: ____________________

## Technology Used
| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS, JavaScript (Fetch API) |
| Backend | Python, FastAPI, Pydantic |
| Database | MySQL |
| Chatbot | Rule-based Python function (no live AI) |

## Features
- Browse Python questions with category and difficulty, and filter by either
- View a question with its description, sample input and expected output
- Submit an answer (auto-checked against the expected output) or mark a question as completed
- Every attempt and score is stored in MySQL
- Progress page: questions attempted, completed, average score and recent attempts
- Rule-based chatbot for Python, REST API, FastAPI, MySQL and interview questions
- Friendly messages for empty input, missing records and an unavailable backend
- Optional: `POST /questions` lets an administrator add questions (use `/docs`)

## Project Structure
```
smart-placement-assistant/
├── backend/        FastAPI app (main.py, database.py, schemas.py, chatbot.py)
├── frontend/       HTML, CSS and JavaScript pages
├── database/       schema.sql and seed.sql
├── screenshots/
└── README.md
```

## Setup Instructions

### 1. Database
1. Open MySQL Workbench and connect to your local server.
2. Run `database/schema.sql`, then `database/seed.sql`.
3. Check: `SELECT COUNT(*) FROM placement_assistant.questions;` should return 10.

### 2. Backend
```
cd backend
python -m venv venv
source venv/Scripts/activate      # Git Bash on Windows
# venv\Scripts\activate           # Windows Command Prompt
# source venv/bin/activate        # Mac / Linux
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and put your own MySQL password in it (never commit `.env`).

Start the server:
```
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs to test the API.

### 3. Frontend
Open a **second** terminal:
```
cd frontend
python -m http.server 5501
```
Then open http://127.0.0.1:5501/index.html in your browser.

## API Endpoints

| Method | Endpoint | Purpose | Success | Errors |
|--------|----------|---------|---------|--------|
| GET | `/` | Check backend is running | 200 | - |
| GET | `/questions` | List questions (optional `?category=` and `?difficulty=`) | 200 | 500 |
| GET | `/questions/{question_id}` | Get one question | 200 | 404, 422 |
| POST | `/questions` | Add a question (optional admin feature) | 201 | 422 |
| POST | `/attempts` | Save an attempt or completion | 201 | 400, 404, 422 |
| GET | `/students/{student_id}/progress` | Progress summary | 200 | 404, 422 |
| POST | `/chat` | Rule-based chatbot reply | 200 | 400, 422 |

### Sample requests and responses

**GET /questions/1**
```json
{
  "question_id": 1,
  "title": "Reverse a string",
  "category": "Strings",
  "difficulty": "Beginner",
  "description": "Write a function that returns the reverse of a given string.",
  "sample_input": "hello",
  "expected_output": "olleh"
}
```

**GET /questions/999** -> 404
```json
{ "detail": "Question not found" }
```

**POST /attempts** - request
```json
{ "student_id": 1, "question_id": 1, "submitted_answer": "olleh", "mark_completed": false }
```
Response (201)
```json
{
  "attempt_id": 1, "student_id": 1, "question_id": 1,
  "score": 100.0, "completed": true,
  "message": "Correct! Your answer matches the expected output."
}
```
Send `{"student_id": 1, "question_id": 3, "mark_completed": true}` to mark a question completed without an answer.
An empty answer without `mark_completed` returns 400; an unknown student or question returns 404.

**GET /students/1/progress** - response (200)
```json
{
  "student_id": 1, "student_name": "Demo Student",
  "total_questions": 10, "total_attempts": 2,
  "questions_attempted": 2, "questions_completed": 1,
  "average_score": 50.0,
  "recent_attempts": [
    { "attempt_id": 2, "question_id": 1, "title": "Reverse a string",
      "score": 100.0, "completed": true, "attempted_at": "2026-11-07T10:30:00" }
  ]
}
```

**POST /chat** - request
```json
{ "message": "What is FastAPI?" }
```
Response (200)
```json
{ "reply": "FastAPI is a modern Python framework for building APIs. ..." }
```

## Scoring Rule
The app never runs a student's code (that would be unsafe). A submitted answer is compared with the question's expected output, ignoring case and whitespace: a match scores 100 and completes the question, otherwise the attempt is saved with a score of 0. "Mark as Completed" records a score of 100.

## Rule-Based Chatbot vs Generative AI
The chatbot in this project is **rule-based**: `chatbot.py` checks the message for known keywords and returns a predefined answer. It cannot reason about new questions, and it is **not Generative AI**. A Large Language Model (LLM) generates a new answer for any question. To upgrade later, replace the body of `get_reply()` with a call to an LLM API from the backend, keep the API key in `.env` on the server, and note that API calls can cost money. Chatbot answers are suggestions, not guaranteed interview advice.

## Security Notes
- All SQL uses parameterised queries (`%s`), never string concatenation.
- Inputs are validated on the backend with Pydantic.
- Database credentials are in `.env`, which is excluded by `.gitignore`.
- The frontend renders text with `textContent`, so typed HTML is not executed.
- CORS is open (`*`) for classroom use; restrict it in a real deployment.

## Known Limitations
- No login: a seeded demo student (ID 1) is used for all attempts.
- Answers are checked by comparing text, not by running code.
- The chatbot only knows a fixed set of topics.
- Progress shows only the last 20 attempts.

## Team Contributions
| Member | Contribution |
|--------|-------------|
|        |             |

## Screenshots
See the `screenshots/` folder: question list, question detail, progress page and chatbot.
