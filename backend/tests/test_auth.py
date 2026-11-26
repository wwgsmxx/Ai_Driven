import time

from app.core.deps import get_token_verifier
from app.core.security import AuthUnavailableError
from app.models.user import User


def test_missing_token_returns_401(client):
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/quizzes").status_code == 401


def test_garbage_token_returns_401(client, bearer):
    r = client.get("/api/auth/me", headers=bearer("not-a-jwt"))
    assert r.status_code == 401


def test_expired_token_returns_401(client, make_token, bearer):
    token = make_token(exp=int(time.time()) - 10)
    assert client.get("/api/auth/me", headers=bearer(token)).status_code == 401


def test_wrong_issuer_and_audience_return_401(client, make_token, bearer):
    bad_iss = make_token(iss="http://evil.local/realms/quizai")
    bad_aud = make_token(aud="other-api")
    assert client.get("/api/auth/me", headers=bearer(bad_iss)).status_code == 401
    assert client.get("/api/auth/me", headers=bearer(bad_aud)).status_code == 401


def test_wrong_signing_key_returns_401(client, make_wrong_key_token, bearer):
    bad_key_token = make_wrong_key_token()
    assert client.get("/api/auth/me", headers=bearer(bad_key_token)).status_code == 401


def test_token_without_app_role_returns_403(client, make_token, bearer):
    token = make_token(roles=("default-roles-quizai",))
    assert client.get("/api/auth/me", headers=bearer(token)).status_code == 403


def test_first_login_creates_user_and_syncs_role(client, make_token, bearer):
    token = make_token(
        sub="kc-1",
        email="aru@demo.kz",
        roles=("student", "teacher"),
    )
    r = client.get("/api/auth/me", headers=bearer(token))
    assert r.status_code == 200
    assert r.json()["email"] == "aru@demo.kz"
    assert r.json()["role"] == "teacher"  # APP_ROLES тәртібі бойынша жоғарғысы


def test_legacy_seed_user_linked_on_first_login(client, db, make_token, bearer):
    legacy = User(
        keycloak_id="legacy-1",
        email="teacher@demo.kz",
        full_name="Old Name",
        role="student",
    )
    db.add(legacy)
    db.commit()
    db.refresh(legacy)
    legacy_id = legacy.id

    token = make_token(
        sub="kc-real-uuid-123",
        email="teacher@demo.kz",
        roles=("teacher",),
    )
    r = client.get("/api/auth/me", headers=bearer(token))
    assert r.status_code == 200
    assert r.json()["id"] == legacy_id
    assert r.json()["role"] == "teacher"

    db.refresh(legacy)
    assert legacy.keycloak_id == "kc-real-uuid-123"


def test_student_cannot_create_quiz_or_list_users(client, make_token, bearer):
    student_headers = bearer(
        make_token(sub="kc-s", email="s@demo.kz", roles=("student",))
    )
    assert (
        client.post(
            "/api/quizzes",
            json={"title": "Алгебра", "topic": "Математика"},
            headers=student_headers,
        ).status_code
        == 403
    )
    assert client.get("/api/users", headers=student_headers).status_code == 403


def test_teacher_cannot_modify_foreign_quiz_or_list_users(client, make_token, bearer):
    t1_headers = bearer(make_token(sub="kc-t1", email="t1@demo.kz", roles=("teacher",)))
    t2_headers = bearer(make_token(sub="kc-t2", email="t2@demo.kz", roles=("teacher",)))

    created = client.post(
        "/api/quizzes",
        json={"title": "Алгебра", "topic": "Математика"},
        headers=t1_headers,
    )
    assert created.status_code == 201
    quiz_id = created.json()["id"]

    # Бөтен мұғалім өзгерте/өшіре алмайды -> 403
    assert (
        client.patch(
            f"/api/quizzes/{quiz_id}",
            json={"title": "Hack"},
            headers=t2_headers,
        ).status_code
        == 403
    )
    assert client.get("/api/users", headers=t1_headers).status_code == 403


def test_keycloak_unavailable_returns_503(client, make_token, bearer):
    class _UnavailableVerifier:
        def verify(self, token: str):
            raise AuthUnavailableError("Keycloak кілтін алу мүмкін емес")

    client.app.dependency_overrides[get_token_verifier] = _UnavailableVerifier
    r = client.get("/api/auth/me", headers=bearer(make_token()))
    assert r.status_code == 503
