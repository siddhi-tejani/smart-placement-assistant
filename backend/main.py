from typing import List, Optional

import mysql.connector
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from chatbot import get_reply
from database import db_cursor
from schemas import (
    AttemptCreate,
    AttemptOut,
    ChatRequest,
    ChatResponse,
    ProgressOut,
    Question,
    QuestionCreate,
)

app = FastAPI(title="Smart Placement Preparation Assistant")

# Allow the browser page (served from another port) to call this API.
# "*" is fine for a classroom project; restrict it for real deployments.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(mysql.connector.Error)
async def database_error_handler(request, exc):
    # Any MySQL problem becomes a clean 500 message (details stay in the terminal).
    print("Database error:", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error. Please try again later."},
    )


def normalize(text: Optional[str]) -> str:
    """Lower-case and remove all whitespace so '1 2 3' == '1  2 3'."""
    return "".join((text or "").lower().split())


# ---------------------------------------------------------------- Home
@app.get("/")
def home():
    return {"message": "Backend is running"}


# ----------------------------------------------------------- Questions
@app.get("/questions", response_model=List[Question])
def list_questions(category: Optional[str] = None, difficulty: Optional[str] = None):
    query = "SELECT * FROM questions WHERE 1=1"
    params = []
    if category:
        query += " AND category = %s"
        params.append(category)
    if difficulty:
        query += " AND difficulty = %s"
        params.append(difficulty)
    query += " ORDER BY question_id"

    with db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


@app.get("/questions/{question_id}", response_model=Question)
def get_question(question_id: int):
    with db_cursor() as cursor:
        cursor.execute("SELECT * FROM questions WHERE question_id = %s", (question_id,))
        row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return row


@app.post("/questions", response_model=Question, status_code=201)
def add_question(question: QuestionCreate):
    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO questions (title, category, difficulty, description, "
            "sample_input, expected_output) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                question.title.strip(),
                question.category.strip(),
                question.difficulty,
                question.description.strip(),
                question.sample_input,
                question.expected_output,
            ),
        )
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM questions WHERE question_id = %s", (new_id,))
        return cursor.fetchone()


# ------------------------------------------------------------ Attempts
@app.post("/attempts", response_model=AttemptOut, status_code=201)
def save_attempt(attempt: AttemptCreate):
    answer = (attempt.submitted_answer or "").strip()
    if not answer and not attempt.mark_completed:
        raise HTTPException(
            status_code=400,
            detail="Please type an answer or mark the question as completed.",
        )

    with db_cursor(commit=True) as cursor:
        cursor.execute(
            "SELECT student_id FROM students WHERE student_id = %s",
            (attempt.student_id,),
        )
        if cursor.fetchone() is None:
            raise HTTPException(status_code=404, detail="Student not found")

        cursor.execute(
            "SELECT expected_output FROM questions WHERE question_id = %s",
            (attempt.question_id,),
        )
        question = cursor.fetchone()
        if question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        # Scoring rule (simple and safe: we never run the student's code):
        #  - "Mark as completed" -> full marks
        #  - otherwise compare the answer with the expected output
        if attempt.mark_completed:
            score, completed = 100, True
            message = "Question marked as completed."
        elif normalize(answer) == normalize(question["expected_output"]):
            score, completed = 100, True
            message = "Correct! Your answer matches the expected output."
        else:
            score, completed = 0, False
            message = "Attempt saved, but the answer does not match the expected output."

        cursor.execute(
            "INSERT INTO attempts (student_id, question_id, submitted_answer, score, completed) "
            "VALUES (%s, %s, %s, %s, %s)",
            (
                attempt.student_id,
                attempt.question_id,
                answer or None,
                score,
                completed,
            ),
        )
        attempt_id = cursor.lastrowid

    return AttemptOut(
        attempt_id=attempt_id,
        student_id=attempt.student_id,
        question_id=attempt.question_id,
        score=score,
        completed=completed,
        message=message,
    )


# ------------------------------------------------------------ Progress
@app.get("/students/{student_id}/progress", response_model=ProgressOut)
def get_progress(student_id: int):
    with db_cursor() as cursor:
        cursor.execute(
            "SELECT full_name FROM students WHERE student_id = %s", (student_id,)
        )
        student = cursor.fetchone()
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")

        cursor.execute("SELECT COUNT(*) AS total FROM questions")
        total_questions = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total_attempts, "
            "COUNT(DISTINCT question_id) AS questions_attempted, "
            "COUNT(DISTINCT CASE WHEN completed = TRUE THEN question_id END) AS questions_completed, "
            "COALESCE(AVG(score), 0) AS average_score "
            "FROM attempts WHERE student_id = %s",
            (student_id,),
        )
        summary = cursor.fetchone()

        cursor.execute(
            "SELECT a.attempt_id, a.question_id, q.title, a.score, a.completed, a.attempted_at "
            "FROM attempts a JOIN questions q ON q.question_id = a.question_id "
            "WHERE a.student_id = %s "
            "ORDER BY a.attempted_at DESC, a.attempt_id DESC LIMIT 20",
            (student_id,),
        )
        recent = cursor.fetchall()

    return ProgressOut(
        student_id=student_id,
        student_name=student["full_name"],
        total_questions=total_questions,
        total_attempts=summary["total_attempts"],
        questions_attempted=summary["questions_attempted"],
        questions_completed=summary["questions_completed"],
        average_score=round(float(summary["average_score"]), 2),
        recent_attempts=recent,
    )


# ---------------------------------------------------------------- Chat
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    return ChatResponse(reply=get_reply(request.message))
