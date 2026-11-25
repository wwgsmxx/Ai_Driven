from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AttemptCreate(BaseModel):
    answers: list[int] = Field(..., min_length=1)


class AttemptRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_id: int
    student_id: int
    answers: list[int]
    score: int
    total: int
    created_at: datetime
