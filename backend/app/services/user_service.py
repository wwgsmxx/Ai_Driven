from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserRead, UserUpdate
from app.services.errors import BadRequestError, NotFoundError


class UserService:
    def __init__(self, repo: UserRepository) -> None:
        self.repo = repo

    def _get(self, user_id: int) -> User:
        user = self.repo.get(user_id)
        if user is None:
            raise NotFoundError(f"Пайдаланушы табылмады: id={user_id}")
        return user

    def list_users(self, *, skip: int = 0, limit: int = 100) -> list[UserRead]:
        users = self.repo.list(skip=skip, limit=limit)
        return [UserRead.model_validate(u) for u in users]

    def get_user(self, user_id: int) -> UserRead:
        return UserRead.model_validate(self._get(user_id))

    def update_user(
        self,
        user_id: int,
        data: UserUpdate,
        current_user: User,
    ) -> UserRead:
        target = self._get(user_id)
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        if (
            "role" in changes
            and target.id == current_user.id
            and changes["role"] != current_user.role
        ):
            raise BadRequestError("Өз рөліңізді өзгерте алмайсыз")

        for field, value in changes.items():
            setattr(target, field, value)
        return UserRead.model_validate(self.repo.save(target))

    def delete_user(self, user_id: int, current_user: User) -> None:
        target = self._get(user_id)
        if target.id == current_user.id:
            raise BadRequestError("Өзіңізді өшіре алмайсыз")
        self.repo.delete(target)
