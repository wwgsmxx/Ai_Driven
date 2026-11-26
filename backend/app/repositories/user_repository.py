from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import Identity
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, *, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = select(User).order_by(User.id.asc()).offset(skip).limit(limit)
        return list(self.db.scalars(stmt).all())

    def get(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email))

    def get_by_keycloak_id(self, keycloak_id: str) -> User | None:
        return self.db.scalar(
            select(User).where(User.keycloak_id == keycloak_id)
        )

    def sync(self, identity: Identity, role: str) -> User:
        user = self.get_by_keycloak_id(identity.keycloak_id)
        if user is None:
            # 8-сабақтан қалған seed-пайдаланушыны email бойынша байланыстырамыз
            legacy = self.get_by_email(identity.email)
            if legacy is not None and legacy.keycloak_id.startswith("legacy-"):
                legacy.keycloak_id = identity.keycloak_id
                legacy.full_name = identity.full_name
                legacy.role = role
                self.db.commit()
                self.db.refresh(legacy)
                return legacy
            user = User(
                keycloak_id=identity.keycloak_id,
                email=identity.email,
                full_name=identity.full_name,
                role=role,
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user

        if (user.email, user.full_name, user.role) != (
            identity.email,
            identity.full_name,
            role,
        ):
            user.email = identity.email
            user.full_name = identity.full_name
            user.role = role
            self.db.commit()
            self.db.refresh(user)
        return user

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
