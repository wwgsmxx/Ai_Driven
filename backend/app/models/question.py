from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import JSON

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.quiz import Quiz


class Question(Base):
    __tablename__ = "questions"
    __table_args__ = (
        CheckConstraint(
            "source IN ('manual', 'ai', 'fallback')",
            name="ck_questions_source",
        ),
        CheckConstraint(
            "correct_index >= 0",
            name="ck_questions_correct_index",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    quiz_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("quizzes.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    position: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[Any] = mapped_column(
        JSON().with_variant(JSONB, "postgresql"),
        nullable=False,
    )
    correct_index: Mapped[int] = mapped_column(Integer, nullable=False)
    source: Mapped[str] = mapped_column(
        String(20),
        default="manual",
        nullable=False,
    )

    quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")
