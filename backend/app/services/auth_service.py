from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.user import UserRead
from app.services.errors import AuthError, ConflictError


class AuthService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def register(self, data: RegisterRequest) -> UserRead:
        existing = self.repo.get_by_email(data.email)
        if existing is not None:
            raise ConflictError("Бұл email бұрыннан тіркелген")

        user = User(
            email=data.email,
            full_name=data.full_name,
            password_hash=hash_password(data.password),
            role="student",
        )
        return UserRead.model_validate(self.repo.create(user))

    def login(self, data: LoginRequest) -> LoginResponse:
        user = self.repo.get_by_email(data.email)
        if (
            user is None
            or not user.password_hash
            or not verify_password(data.password, user.password_hash)
        ):
            raise AuthError("Email немесе құпиясөз қате")

        return LoginResponse(
            message="Кіру сәтті тексерілді",
            user=UserRead.model_validate(user),
        )
