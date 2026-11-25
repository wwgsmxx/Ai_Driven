from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.question import QuestionForStudent, QuestionForTeacher


class QuizCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    topic: Optional[str] = Field(default=None, min_length=1, max_length=120)


class QuizUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=200)
    topic: Optional[str] = Field(default=None, min_length=1, max_length=120)


class QuizRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    topic: Optional[str]
    owner_id: int
    is_published: bool
    created_at: datetime


class QuizForTeacher(QuizRead):
    questions: list[QuestionForTeacher] = []


class QuizForStudent(QuizRead):
    questions: list[QuestionForStudent] = []
