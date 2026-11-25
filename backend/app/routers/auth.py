from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.deps import get_auth_service
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserRead:
    return service.register(data)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
def login(
    data: LoginRequest,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    return service.login(data)
