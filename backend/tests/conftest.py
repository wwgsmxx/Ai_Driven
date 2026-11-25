import pytest
from fastapi.testclient import TestClient

from app.core.config import settings

# Тесттер кестелерді өшіріп-қайта жасайды -> тек
# бөлек тест-дерекқорда: quizai -> quizai_test
if not settings.database_url.endswith("_test"):
    settings.database_url += "_test"

import app.models  # noqa: E402,F401
from app.core.database import Base, SessionLocal, engine  # noqa: E402
from app.core.deps import get_current_user  # noqa: E402
from app.main import app  # noqa: E402
from app.models.user import User  # noqa: E402


@pytest.fixture(autouse=True)
def clean_state():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    app.dependency_overrides.clear()
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
    def _make_user(email: str, role: str = "student", full_name: str = "User") -> User:
        user = User(email=email, role=role, full_name=full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    return _make_user


@pytest.fixture
def auth_as():
    def _auth_as(user: User) -> None:
        app.dependency_overrides[get_current_user] = lambda: user

    return _auth_as
