from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jwt
from jwt import PyJWKClient, PyJWKClientError

from app.core.config import settings

# Жобаның рөлдері маңыздылығы бойынша: бір пайдаланушыда екеуі болса — жоғарғысы
APP_ROLES = ("admin", "teacher", "student")


class AuthUnavailableError(Exception):
    pass


@dataclass(frozen=True)
class Identity:
    keycloak_id: str
    email: str
    full_name: str
    role: str | None


class KeycloakVerifier:
    def __init__(self) -> None:
        self._jwks = PyJWKClient(settings.jwks_url, cache_keys=True)

    def verify(self, token: str) -> dict[str, Any]:
        try:
            key = self._jwks.get_signing_key_from_jwt(token).key
        except PyJWKClientError as exc:
            raise AuthUnavailableError("Keycloak кілтін алу мүмкін емес") from exc
        return jwt.decode(
            token,
            key=key,
            algorithms=["RS256"],
            issuer=settings.keycloak_issuer,
            audience=settings.keycloak_audience,
            options={"require": ["exp", "iat", "iss", "sub", "aud"]},
        )


def identity_from_claims(claims: dict[str, Any]) -> Identity:
    raw_roles = set(claims.get("realm_access", {}).get("roles") or [])
    role = next((r for r in APP_ROLES if r in raw_roles), None)
    sub = str(claims["sub"])
    email = (
        claims.get("email")
        or claims.get("preferred_username")
        or f"{sub}@keycloak.local"
    )
    full_name = claims.get("name") or email.split("@")[0]
    return Identity(
        keycloak_id=sub,
        email=str(email),
        full_name=str(full_name),
        role=role,
    )
