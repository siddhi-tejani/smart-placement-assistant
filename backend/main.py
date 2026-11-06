from typing import List, Optional

import mysql.connector
from fastapi import FastAPI, HTTPException

from database import get_connection
from schemas import Question

app = FastAPI(title="Smart Placement Preparation Assistant")


@app.get("/")
def home():
    return {"message": "Backend is running"}


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

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Database error. Please try again later.")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


@app.get("/questions/{question_id}", response_model=Question)
def get_question(question_id: int):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM questions WHERE question_id = %s", (question_id,))
        row = cursor.fetchone()
        cursor.close()
    except mysql.connector.Error:
        raise HTTPException(status_code=500, detail="Database error. Please try again later.")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return row