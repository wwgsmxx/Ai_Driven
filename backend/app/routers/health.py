from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.database import engine
from app.schemas.health import HealthRead

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthRead)
def get_health() -> HealthRead:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db = "up"
    except SQLAlchemyError:
        db = "down"

    return HealthRead(
        status="ok" if db == "up" else "degraded",
        environment=settings.ENVIRONMENT,
        services={"database": db},
    )
