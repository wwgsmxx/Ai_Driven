import pytest

from app.core.config import settings

# Тесттер кестелерді өшіріп-қайта жасайды -> тек
# бөлек тест-дерекқорда: quizai -> quizai_test
if not settings.database_url.endswith("_test"):
    settings.database_url += "_test"

import app.models  # noqa: E402,F401
from app.core.database import Base, engine  # noqa: E402


@pytest.fixture(autouse=True)
def clean_state():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield
