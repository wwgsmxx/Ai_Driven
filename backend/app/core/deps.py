import logging
from collections.abc import Callable
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    AuthUnavailableError,
    KeycloakVerifier,
    identity_from_claims,
)
from app.models.user import User
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.question_repository import QuestionRepository
from app.repositories.quiz_repository import QuizRepository
from app.repositories.user_repository import UserRepository
from app.services.attempt_service import AttemptService
from app.services.errors import AuthError, ForbiddenError
from app.services.question_service import QuestionService
from app.services.quiz_service import QuizService
from app.services.user_service import UserService

log = logging.getLogger(__name__)

# Swagger UI "Authorize" батырмасына Keycloak кіру бетінің мекенжайын береді
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{settings.keycloak_issuer}/protocol/openid-connect/auth",
    tokenUrl=f"{settings.keycloak_issuer}/protocol/openid-connect/token",
    auto_error=False,
)

_verifier = KeycloakVerifier()


def get_token_verifier() -> KeycloakVerifier:
    return _verifier


def get_current_user(
    token: Annotated[Optional[str], Depends(oauth2_scheme)],
    verifier: Annotated[KeycloakVerifier, Depends(get_token_verifier)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    if not token:
        raise AuthError("Токен берілмеді")
    try:
        claims = verifier.verify(token)
    except AuthUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except jwt.ExpiredSignatureError as exc:
        raise AuthError("Токеннің мерзімі өтіп кетті") from exc
    except jwt.InvalidTokenError as exc:
        # Токеннің өзі логқа ЖАЗЫЛМАЙДЫ — тек қате класы
        log.warning("Жарамсыз JWT: %s", type(exc).__name__)
        raise AuthError("Токен жарамсыз") from exc

    identity = identity_from_claims(claims)
    if identity.role is None:
        raise ForbiddenError("Токенде қосымша рөлі көрсетілмеген")
    return UserRepository(db).sync(identity, identity.role)


def require_role(*roles: str) -> Callable[[User], User]:
    def role_checker(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if current_user.role not in roles:
            raise ForbiddenError("Бұл әрекетті орындауға рұқсат жоқ")
        return current_user

    return role_checker


def get_user_service(db: Annotated[Session, Depends(get_db)]) -> UserService:
    return UserService(UserRepository(db))


def get_quiz_service(db: Annotated[Session, Depends(get_db)]) -> QuizService:
    return QuizService(QuizRepository(db), QuestionRepository(db))


def get_question_service(db: Annotated[Session, Depends(get_db)]) -> QuestionService:
    return QuestionService(QuestionRepository(db), QuizRepository(db))


def get_attempt_service(db: Annotated[Session, Depends(get_db)]) -> AttemptService:
    return AttemptService(
        AttemptRepository(db),
        QuizRepository(db),
        QuestionRepository(db),
    )
