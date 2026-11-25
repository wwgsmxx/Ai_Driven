from app.models.attempt import Attempt
from app.models.user import User
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.question_repository import QuestionRepository
from app.repositories.quiz_repository import QuizRepository
from app.schemas.attempt import AttemptCreate, AttemptRead
from app.services.errors import BadRequestError, NotFoundError


class AttemptService:
    def __init__(
        self,
        repo: AttemptRepository,
        quiz_repo: QuizRepository,
        question_repo: QuestionRepository,
    ) -> None:
        self.repo = repo
        self.quiz_repo = quiz_repo
        self.question_repo = question_repo

    def submit_attempt(
        self,
        quiz_id: int,
        data: AttemptCreate,
        user: User,
    ) -> AttemptRead:
        quiz = self.quiz_repo.get(quiz_id)
        if quiz is None:
            raise NotFoundError(f"Тест табылмады: id={quiz_id}")
        if not quiz.is_published:
            raise BadRequestError("Жарияланбаған тестті тапсыруға болмайды")

        questions = self.question_repo.list_by_quiz(quiz_id)
        if len(data.answers) != len(questions):
            raise BadRequestError("Жауаптар саны сұрақтар санына сәйкес емес")

        score = sum(
            1
            for q, selected in zip(questions, data.answers)
            if selected == q.correct_index
        )
        attempt = Attempt(
            quiz_id=quiz_id,
            student_id=user.id,
            answers=data.answers,
            score=score,
            total=len(questions),
        )
        return AttemptRead.model_validate(self.repo.create(attempt))

    def list_my_attempts(
        self,
        user: User,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[AttemptRead]:
        attempts = self.repo.list_by_student(user.id, skip=skip, limit=limit)
        return [AttemptRead.model_validate(a) for a in attempts]
