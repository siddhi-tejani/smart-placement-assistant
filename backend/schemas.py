from typing import Optional
from pydantic import BaseModel


class Question(BaseModel):
    question_id: int
    title: str
    category: str
    difficulty: Optional[str] = None
    description: str
    sample_input: Optional[str] = None
    expected_output: Optional[str] = None