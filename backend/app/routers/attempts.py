from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import get_attempt_service, require_role
from app.models.user import User
from app.schemas.attempt import AttemptCreate, AttemptRead
from app.services.attempt_service import AttemptService

router = APIRouter(prefix="/api", tags=["attempts"])


@router.post(
    "/quizzes/{quiz_id}/attempts",
    response_model=AttemptRead,
    status_code=status.HTTP_201_CREATED,
)
def submit_attempt(
    quiz_id: int,
    data: AttemptCreate,
    user: Annotated[User, Depends(require_role("student"))],
    service: Annotated[AttemptService, Depends(get_attempt_service)],
) -> AttemptRead:
    return service.submit_attempt(quiz_id=quiz_id, data=data, user=user)


@router.get(
    "/attempts/me",
    response_model=list[AttemptRead],
    status_code=status.HTTP_200_OK,
)
def list_my_attempts(
    user: Annotated[User, Depends(require_role("student"))],
    service: Annotated[AttemptService, Depends(get_attempt_service)],
) -> list[AttemptRead]:
    return service.list_my_attempts(user=user)
