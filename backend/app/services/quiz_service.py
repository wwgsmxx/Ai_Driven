from typing import Optional, Union

from app.models.quiz import Quiz
from app.models.user import User
from app.repositories.question_repository import QuestionRepository
from app.repositories.quiz_repository import QuizRepository
from app.schemas.quiz import (
    QuizCreate,
    QuizForStudent,
    QuizForTeacher,
    QuizRead,
    QuizUpdate,
)
from app.services.errors import BadRequestError, ForbiddenError, NotFoundError


class QuizService:
    def __init__(
        self,
        repo: QuizRepository,
        question_repo: Optional[QuestionRepository] = None,
    ) -> None:
        self.repo = repo
        self.question_repo = question_repo

    def _get(self, quiz_id: int) -> Quiz:
        quiz = self.repo.get(quiz_id)
        if quiz is None:
            raise NotFoundError(f"Тест табылмады: id={quiz_id}")
        return quiz

    def _get_own(self, quiz_id: int, user: User) -> Quiz:
        quiz = self._get(quiz_id)
        if quiz.owner_id != user.id and user.role != "admin":
            raise ForbiddenError("Бұл тест сіздікі емес")
        return quiz

    def list_quizzes(
        self,
        user: User,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[QuizRead]:
        quizzes = self.repo.list_for_user(
            role=user.role,
            user_id=user.id,
            skip=skip,
            limit=limit,
        )
        return [QuizRead.model_validate(q) for q in quizzes]

    def get_quiz(
        self,
        quiz_id: int,
        user: User,
    ) -> Union[QuizForTeacher, QuizForStudent]:
        quiz = self.repo.get_with_questions(quiz_id)
        if quiz is None:
            raise NotFoundError(f"Тест табылмады: id={quiz_id}")
        if not quiz.is_published and quiz.owner_id != user.id and user.role != "admin":
            raise ForbiddenError("Бұл тестке кіруге рұқсат жоқ")

        quiz.questions.sort(key=lambda q: (q.position, q.id))
        if quiz.owner_id == user.id or user.role == "admin":
            return QuizForTeacher.model_validate(quiz)
        return QuizForStudent.model_validate(quiz)

    def create_quiz(self, data: QuizCreate, user: User) -> QuizRead:
        if user.role not in ("teacher", "admin"):
            raise ForbiddenError("Тек мұғалім тест құра алады")
        quiz = Quiz(
            title=data.title,
            topic=data.topic,
            owner_id=user.id,
            is_published=False,
        )
        return QuizRead.model_validate(self.repo.create(quiz))

    def update_quiz(self, quiz_id: int, data: QuizUpdate, user: User) -> QuizRead:
        quiz = self._get_own(quiz_id, user)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        for field, value in changes.items():
            setattr(quiz, field, value)
        return QuizRead.model_validate(self.repo.save(quiz))

    def publish_quiz(self, quiz_id: int, user: User) -> QuizRead:
        quiz = self._get_own(quiz_id, user)
        if self.question_repo is not None:
            count = self.question_repo.count_by_quiz(quiz_id)
        else:
            loaded = self.repo.get_with_questions(quiz_id)
            count = len(loaded.questions) if loaded else 0

        if count == 0:
            raise BadRequestError("Сұрақсыз тестті жариялауға болмайды")
        quiz.is_published = True
        return QuizRead.model_validate(self.repo.save(quiz))

    def delete_quiz(self, quiz_id: int, user: User) -> None:
        quiz = self._get_own(quiz_id, user)
        self.repo.delete(quiz)
