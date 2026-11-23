from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.quiz import Quiz
    from app.models.user import User


class Attempt(Base):
    __tablename__ = "attempts"
    __table_args__ = (
        CheckConstraint("score >= 0", name="ck_attempts_score"),
        CheckConstraint("total >= 0", name="ck_attempts_total"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    answers: Mapped[Any] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
    )
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="attempts")
    student: Mapped["User"] = relationship("User", back_populates="attempts")
