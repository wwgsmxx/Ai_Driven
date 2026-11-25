from typing import Annotated, Union

from fastapi import APIRouter, Depends, status

from app.core.deps import get_quiz_service, require_role
from app.models.user import User
from app.schemas.quiz import (
    QuizCreate,
    QuizForStudent,
    QuizForTeacher,
    QuizRead,
    QuizUpdate,
)
from app.services.quiz_service import QuizService

router = APIRouter(prefix="/api/quizzes", tags=["quizzes"])


@router.get("", response_model=list[QuizRead], status_code=status.HTTP_200_OK)
def list_quizzes(
    user: Annotated[User, Depends(require_role("student", "teacher", "admin"))],
    service: Annotated[QuizService, Depends(get_quiz_service)],
) -> list[QuizRead]:
    return service.list_quizzes(user=user)


@router.post("", response_model=QuizRead, status_code=status.HTTP_201_CREATED)
def create_quiz(
    data: QuizCreate,
    user: Annotated[User, Depends(require_role("teacher", "admin"))],
    service: Annotated[QuizService, Depends(get_quiz_service)],
) -> QuizRead:
    return service.create_quiz(data=data, user=user)


@router.get(
    "/{quiz_id}",
    response_model=Union[QuizForTeacher, QuizForStudent],
    status_code=status.HTTP_200_OK,
)
def get_quiz(
    quiz_id: int,
    user: Annotated[User, Depends(require_role("student", "teacher", "admin"))],
    service: Annotated[QuizService, Depends(get_quiz_service)],
) -> Union[QuizForTeacher, QuizForStudent]:
    return service.get_quiz(quiz_id=quiz_id, user=user)


@router.patch("/{quiz_id}", response_model=QuizRead, status_code=status.HTTP_200_OK)
def update_quiz(
    quiz_id: int,
    data: QuizUpdate,
    user: Annotated[User, Depends(require_role("teacher", "admin"))],
    service: Annotated[QuizService, Depends(get_quiz_service)],
) -> QuizRead:
    return service.update_quiz(quiz_id=quiz_id, data=data, user=user)


@router.delete("/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quiz(
    quiz_id: int,
    user: Annotated[User, Depends(require_role("teacher", "admin"))],
    service: Annotated[QuizService, Depends(get_quiz_service)],
) -> None:
    service.delete_quiz(quiz_id=quiz_id, user=user)


@router.post(
    "/{quiz_id}/publish",
    response_model=QuizRead,
    status_code=status.HTTP_200_OK,
)
def publish_quiz(
    quiz_id: int,
    user: Annotated[User, Depends(require_role("teacher", "admin"))],
    service: Annotated[QuizService, Depends(get_quiz_service)],
) -> QuizRead:
    return service.publish_quiz(quiz_id=quiz_id, user=user)
