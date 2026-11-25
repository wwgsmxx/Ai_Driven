from typing import Any, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=("../.env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    PROJECT_NAME: str = "QuizAI"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    demo_user_email: str = "teacher@demo.kz"

    # Database (PostgreSQL)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "quizai"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "quizai"
    DATABASE_URL: Optional[str] = None
    database_url: str = ""

    # LLM (Ollama)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"

    def model_post_init(self, __context: Any) -> None:
        if not self.database_url:
            if self.DATABASE_URL:
                self.database_url = self.DATABASE_URL
            else:
                self.database_url = (
                    f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                    f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
                )
        # Docker (127.0.0.1:5432) кезінде localhost IPv6-ға тірелмеуі үшін
        if "@localhost:" in self.database_url:
            self.database_url = self.database_url.replace(
                "@localhost:", "@127.0.0.1:", 1
            )

    @property
    def environment(self) -> str:
        return self.ENVIRONMENT


settings = Settings()
