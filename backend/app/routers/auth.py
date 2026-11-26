from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import get_user_service
from app.schemas.user import UserLogin, UserRead, UserRegister
from app.services.user_service import UserService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserRegister,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    return service.register(data)


@router.post(
    "/login",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
)
def login(
    data: UserLogin,
    service: Annotated[UserService, Depends(get_user_service)],
) -> UserRead:
    return service.check_login(data)
