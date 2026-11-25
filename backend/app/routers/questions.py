from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import get_question_service, require_role
from app.models.user import User
from app.schemas.question import QuestionCreate, QuestionForTeacher, QuestionUpdate
from app.services.question_service import QuestionService

router = APIRouter(prefix="/api", tags=["questions"])


@router.post(
    "/quizzes/{quiz_id}/questions",
    response_model=QuestionForTeacher,
    status_code=status.HTTP_201_CREATED,
)
def add_question(
    quiz_id: int,
    data: QuestionCreate,
    user: Annotated[User, Depends(require_role("teacher", "admin"))],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> QuestionForTeacher:
    return service.add_question(quiz_id=quiz_id, data=data, user=user)


@router.patch(
    "/questions/{question_id}",
    response_model=QuestionForTeacher,
    status_code=status.HTTP_200_OK,
)
def update_question(
    question_id: int,
    data: QuestionUpdate,
    user: Annotated[User, Depends(require_role("teacher", "admin"))],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> QuestionForTeacher:
    return service.update_question(question_id=question_id, data=data, user=user)


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: int,
    user: Annotated[User, Depends(require_role("teacher", "admin"))],
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> None:
    service.delete_question(question_id=question_id, user=user)
