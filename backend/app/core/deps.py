from collections.abc import Callable
from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.question_repository import QuestionRepository
from app.repositories.quiz_repository import QuizRepository
from app.repositories.user_repository import UserRepository
from app.services.attempt_service import AttemptService
from app.services.auth_service import AuthService
from app.services.errors import AuthError, ForbiddenError
from app.services.question_service import QuestionService
from app.services.quiz_service import QuizService
from app.services.user_service import UserService


def get_current_user(db: Annotated[Session, Depends(get_db)]) -> User:
    user = db.scalar(select(User).where(User.email == settings.demo_user_email))
    if user is None:
        raise AuthError("Демо пайдаланушы табылмады")
    return user


def require_role(*roles: str) -> Callable[[User], User]:
    def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in roles:
            raise ForbiddenError("Бұл әрекетті орындауға рұқсат жоқ")
        return current_user

    return role_checker


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(UserRepository(db))


def get_auth_service(db: Annotated[Session, Depends(get_db)]) -> AuthService:
    return AuthService(UserRepository(db))


def get_quiz_service(db: Annotated[Session, Depends(get_db)]) -> QuizService:
    return QuizService(QuizRepository(db), QuestionRepository(db))


def get_question_service(db: Annotated[Session, Depends(get_db)]) -> QuestionService:
    return QuestionService(QuestionRepository(db), QuizRepository(db))


def get_attempt_service(db: Annotated[Session, Depends(get_db)]) -> AttemptService:
    return AttemptService(
        AttemptRepository(db),
        QuizRepository(db),
        QuestionRepository(db),
    )
