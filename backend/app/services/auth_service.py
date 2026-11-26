from app.repositories.user_repository import UserRepository
from app.schemas.user import UserLogin, UserRead
from app.services.user_service import UserService


class AuthService(UserService):
    def __init__(self, repo: UserRepository) -> None:
        super().__init__(repo)

    def login(self, data: UserLogin) -> UserRead:
        return self.check_login(data)
