from fastapi import FastAPI

from app.core.config import settings
from app.routers.health import router as health_router

app = FastAPI(
    title=getattr(settings, "app_name", settings.PROJECT_NAME),
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.include_router(health_router)
