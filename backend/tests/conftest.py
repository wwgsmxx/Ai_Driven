from __future__ import annotations

import time
from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

from app.core.config import settings

# Тесттер кестелерді өшіріп-қайта жасайды -> тек
# бөлек тест-дерекқорда: quizai -> quizai_test
if not settings.database_url.endswith("_test"):
    settings.database_url += "_test"

import app.models  # noqa: E402,F401
from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.core.deps import get_current_user, get_token_verifier  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402

_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)
_PUBLIC_KEY = _PRIVATE_KEY.public_key()
_OTHER_PRIVATE_KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)


class _TestVerifier:
    def verify(self, token: str) -> dict[str, Any]:
        return jwt.decode(
            token,
            key=_PUBLIC_KEY,
            algorithms=["RS256"],
            issuer=settings.keycloak_issuer,
            audience=settings.keycloak_audience,
            options={"require": ["exp", "iat", "iss", "sub", "aud"]},
        )


def _make_token(
    sub: str = "kc-teacher-1",
    email: str = "teacher@demo.kz",
    roles: tuple[str, ...] = ("teacher",),
    *,
    private_key: Any = _PRIVATE_KEY,
    **overrides: Any,
) -> str:
    now = int(time.time())
    payload: dict[str, Any] = {
        "sub": sub,
        "iss": settings.keycloak_issuer,
        "aud": settings.keycloak_audience,
        "iat": now,
        "exp": now + 300,
        "email": email,
        "name": email.split("@")[0],
        "realm_access": {"roles": list(roles)},
        **overrides,
    }
    return jwt.encode(payload, private_key, algorithm="RS256")


def _bearer(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def _make_wrong_key_token(**kwargs: Any) -> str:
    return _make_token(private_key=_OTHER_PRIVATE_KEY, **kwargs)


@pytest.fixture(autouse=True)
def clean_state():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    app.dependency_overrides.clear()
    app.dependency_overrides[get_token_verifier] = _TestVerifier
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def db():
    with SessionLocal() as session:
        yield session


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def make_user(db):
    def _make_user(
        email: str,
        role: str = "student",
        full_name: str = "User",
        keycloak_id: str | None = None,
    ) -> User:
        user = User(
            keycloak_id=keycloak_id or f"kc-{email}",
            email=email,
            role=role,
            full_name=full_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    return _make_user


@pytest.fixture
def make_token():
    return _make_token


@pytest.fixture
def bearer():
    return _bearer


@pytest.fixture
def make_wrong_key_token():
    return _make_wrong_key_token


@pytest.fixture
def auth_as():
    def _auth_as(user: User) -> None:
        app.dependency_overrides[get_current_user] = lambda: user

    return _auth_as
