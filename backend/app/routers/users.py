from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import get_user_service, require_role
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=list[UserRead], status_code=status.HTTP_200_OK)
def list_users(
    _: Annotated[User, Depends(require_role("admin"))],
    service: Annotated[UserService, Depends(get_user_service)],
) -> list[UserRead]:
    return service.list_users()


@router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def get_user(
    user_id: int,
    _: Annotated[User, Depends(require_role("admin"))],
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    return service.get_user(user_id=user_id)


@router.patch("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
def update_user(
    user_id: int,
    data: UserUpdate,
    current_user: Annotated[User, Depends(require_role("admin"))],
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    return service.update_user(user_id=user_id, data=data, current_user=current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(require_role("admin"))],
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    service.delete_user(user_id=user_id, current_user=current_user)
