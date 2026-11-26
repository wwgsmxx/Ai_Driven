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

    # Database (PostgreSQL)
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "quizai"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "quizai"
    DATABASE_URL: Optional[str] = None
    database_url: str = ""

    # Keycloak
    KEYCLOAK_ISSUER: str = "http://localhost:8080/realms/quizai"
    KEYCLOAK_JWKS_URL: Optional[str] = None
    KEYCLOAK_AUDIENCE: str = "quizai-api"
    KEYCLOAK_CLIENT_ID: str = "quizai-web"

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

    @property
    def keycloak_issuer(self) -> str:
        return self.KEYCLOAK_ISSUER

    @property
    def keycloak_audience(self) -> str:
        return self.KEYCLOAK_AUDIENCE

    @property
    def keycloak_client_id(self) -> str:
        return self.KEYCLOAK_CLIENT_ID

    @property
    def jwks_url(self) -> str:
        return (
            self.KEYCLOAK_JWKS_URL
            or f"{self.KEYCLOAK_ISSUER}/protocol/openid-connect/certs"
        )


settings = Settings()
