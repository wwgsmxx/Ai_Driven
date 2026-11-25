import hashlib
import hmac
import secrets

_ITERATIONS = 100_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        _ITERATIONS,
    ).hex()
    return f"{salt}${digest}"


def verify_password(plain_password: str, password_hash: str) -> bool:
    if "$" not in password_hash:
        return False
    salt, expected = password_hash.split("$", 1)
    actual = hashlib.pbkdf2_hmac(
        "sha256",
        plain_password.encode("utf-8"),
        salt.encode("utf-8"),
        _ITERATIONS,
    ).hex()
    return hmac.compare_digest(actual, expected)
