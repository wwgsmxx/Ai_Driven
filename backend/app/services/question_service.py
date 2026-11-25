from app.models.question import Question
from app.models.quiz import Quiz
from app.models.user import User
from app.repositories.question_repository import QuestionRepository
from app.repositories.quiz_repository import QuizRepository
from app.schemas.question import QuestionCreate, QuestionForTeacher, QuestionUpdate
from app.services.errors import BadRequestError, ForbiddenError, NotFoundError


class QuestionService:
    def __init__(
        self,
        repo: QuestionRepository,
        quiz_repo: QuizRepository,
    ) -> None:
        self.repo = repo
        self.quiz_repo = quiz_repo

    def _get_own_quiz(self, quiz_id: int, user: User) -> Quiz:
        quiz = self.quiz_repo.get(quiz_id)
        if quiz is None:
            raise NotFoundError(f"Тест табылмады: id={quiz_id}")
        if quiz.owner_id != user.id and user.role != "admin":
            raise ForbiddenError("Бұл тест сіздікі емес")
        return quiz

    def _get_own_question(self, question_id: int, user: User) -> tuple[Question, Quiz]:
        question = self.repo.get(question_id)
        if question is None:
            raise NotFoundError(f"Сұрақ табылмады: id={question_id}")
        quiz = self._get_own_quiz(question.quiz_id, user)
        return question, quiz

    def add_question(
        self,
        quiz_id: int,
        data: QuestionCreate,
        user: User,
    ) -> QuestionForTeacher:
        quiz = self._get_own_quiz(quiz_id, user)
        if quiz.is_published:
            raise BadRequestError("Жарияланған тестке сұрақ қосуға болмайды")
        if data.correct_index >= len(data.options):
            raise BadRequestError(
                "correct_index нұсқалар санынан кіші болуы тиіс"
            )

        position = (
            data.position
            if data.position is not None
            else self.repo.count_by_quiz(quiz_id) + 1
        )
        question = Question(
            quiz_id=quiz_id,
            position=position,
            text=data.text,
            options=data.options,
            correct_index=data.correct_index,
            source=data.source,
        )
        return QuestionForTeacher.model_validate(self.repo.create(question))

    def update_question(
        self,
        question_id: int,
        data: QuestionUpdate,
        user: User,
    ) -> QuestionForTeacher:
        question, quiz = self._get_own_question(question_id, user)
        if quiz.is_published:
            raise BadRequestError("Жарияланған тесттің сұрағын өзгертуге болмайды")

        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        new_options = changes.get("options", question.options)
        new_correct = changes.get("correct_index", question.correct_index)
        if new_correct >= len(new_options):
            raise BadRequestError(
                "correct_index нұсқалар санынан кіші болуы тиіс"
            )

        for field, value in changes.items():
            setattr(question, field, value)
        return QuestionForTeacher.model_validate(self.repo.save(question))

    def delete_question(self, question_id: int, user: User) -> None:
        question, quiz = self._get_own_question(question_id, user)
        if quiz.is_published:
            raise BadRequestError("Жарияланған тесттің сұрағын өшіруге болмайды")
        self.repo.delete(question)
