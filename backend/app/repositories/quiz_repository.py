from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.quiz import Quiz


class QuizRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(
        self,
        *,
        owner_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Quiz]:
        stmt = select(Quiz).order_by(Quiz.id.desc()).offset(skip).limit(limit)
        if owner_id is not None:
            stmt = stmt.where(Quiz.owner_id == owner_id)
        return list(self.db.scalars(stmt).all())

    def list_for_user(
        self,
        *,
        role: str,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Quiz]:
        stmt = select(Quiz).order_by(Quiz.id.desc())
        if role == "student":
            stmt = stmt.where(Quiz.is_published.is_(True))
        elif role == "teacher":
            stmt = stmt.where(
                or_(Quiz.owner_id == user_id, Quiz.is_published.is_(True))
            )
        stmt = stmt.offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, quiz_id: int) -> Quiz | None:
        return self.db.get(Quiz, quiz_id)

    def get_with_questions(self, quiz_id: int) -> Quiz | None:
        stmt = (
            select(Quiz)
            .options(selectinload(Quiz.questions))
            .where(Quiz.id == quiz_id)
        )
        return self.db.scalar(stmt)

    def create(self, quiz: Quiz) -> Quiz:
        self.db.add(quiz)
        self.db.commit()
        self.db.refresh(quiz)
        return quiz

    def save(self, quiz: Quiz) -> Quiz:
        self.db.add(quiz)
        self.db.commit()
        self.db.refresh(quiz)
        return quiz

    def delete(self, quiz: Quiz) -> None:
        self.db.delete(quiz)
        self.db.commit()
