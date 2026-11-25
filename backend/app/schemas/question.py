from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=3)
    options: list[str] = Field(..., min_length=2, max_length=6)
    correct_index: int = Field(..., ge=0)
    position: Optional[int] = Field(default=None, ge=1)
    source: Literal["manual", "ai", "fallback"] = "manual"


class QuestionUpdate(BaseModel):
    text: Optional[str] = Field(default=None, min_length=3)
    options: Optional[list[str]] = Field(default=None, min_length=2, max_length=6)
    correct_index: Optional[int] = Field(default=None, ge=0)
    position: Optional[int] = Field(default=None, ge=1)


class QuestionForTeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_id: int
    position: int
    text: str
    options: list[str]
    correct_index: int
    source: str


class QuestionForStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_id: int
    position: int
    text: str
    options: list[str]
