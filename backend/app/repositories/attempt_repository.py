from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.attempt import Attempt


class AttemptRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, attempt: Attempt) -> Attempt:
        self.db.add(attempt)
        self.db.commit()
        self.db.refresh(attempt)
        return attempt

    def list_by_student(
        self,
        student_id: int,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Attempt]:
        stmt = (
            select(Attempt)
            .where(Attempt.student_id == student_id)
            .order_by(Attempt.id.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(self.db.scalars(stmt).all())
