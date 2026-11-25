from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.question import Question


class QuestionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_by_quiz(self, quiz_id: int) -> list[Question]:
        stmt = (
            select(Question)
            .where(Question.quiz_id == quiz_id)
            .order_by(Question.position.asc(), Question.id.asc())
        )
        return list(self.db.scalars(stmt).all())

    def count_by_quiz(self, quiz_id: int) -> int:
        stmt = select(func.count()).select_from(Question).where(
            Question.quiz_id == quiz_id
        )
        return int(self.db.scalar(stmt) or 0)

    def get(self, question_id: int) -> Optional[Question]:
        return self.db.get(Question, question_id)

    def create(self, question: Question) -> Question:
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def save(self, question: Question) -> Question:
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def delete(self, question: Question) -> None:
        self.db.delete(question)
        self.db.commit()
