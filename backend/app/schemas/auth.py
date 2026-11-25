from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserRead


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: str = Field(
        ...,
        min_length=5,
        max_length=255,
        pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
    )
    password: str = Field(..., min_length=6, max_length=128)
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=120)


class LoginRequest(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=1, max_length=128)


class LoginResponse(BaseModel):
    message: str
    user: UserRead
