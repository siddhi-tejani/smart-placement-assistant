from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Questions ----------
class Question(BaseModel):
    question_id: int
    title: str
    category: str
    difficulty: Optional[str] = None
    description: str
    sample_input: Optional[str] = None
    expected_output: Optional[str] = None


class QuestionCreate(BaseModel):
    """Request body for POST /questions (optional admin feature)."""
    title: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=60)
    difficulty: str = Field(default="Beginner", max_length=20)
    description: str = Field(min_length=1)
    sample_input: Optional[str] = None
    expected_output: Optional[str] = None


# ---------- Attempts ----------
class AttemptCreate(BaseModel):
    student_id: int = Field(gt=0)
    question_id: int = Field(gt=0)
    submitted_answer: Optional[str] = Field(default=None, max_length=5000)
    mark_completed: bool = False


class AttemptOut(BaseModel):
    attempt_id: int
    student_id: int
    question_id: int
    score: float
    completed: bool
    message: str


# ---------- Progress ----------
class AttemptSummary(BaseModel):
    attempt_id: int
    question_id: int
    title: str
    score: float
    completed: bool
    attempted_at: datetime


class ProgressOut(BaseModel):
    student_id: int
    student_name: str
    total_questions: int
    total_attempts: int
    questions_attempted: int
    questions_completed: int
    average_score: float
    recent_attempts: List[AttemptSummary]


# ---------- Chatbot ----------
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class ChatResponse(BaseModel):
    reply: str
