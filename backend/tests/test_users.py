from app.models.user import User

NEW = {"email": "aru@example.com", "full_name": "Ару", "password": "qwerty-123"}


def test_register_hides_password(client, db):
    r = client.post("/api/auth/register", json=NEW)
    assert r.status_code == 201
    assert "password" not in r.text
    user = db.get(User, r.json()["id"])
    assert user is not None
    assert user.password_hash is not None
    assert user.password_hash.startswith("$argon2id$")


def test_duplicate_email_returns_409(client):
    client.post("/api/auth/register", json=NEW)
    assert client.post("/api/auth/register", json=NEW).status_code == 409


def test_login_checks_password(client):
    client.post("/api/auth/register", json=NEW)
    ok = client.post(
        "/api/auth/login",
        json={"email": NEW["email"], "password": "qwerty-123"},
    )
    bad = client.post(
        "/api/auth/login",
        json={"email": NEW["email"], "password": "wrong-pass"},
    )
    assert ok.status_code == 200
    assert bad.status_code == 401


def test_users_admin_crud(client, make_user, auth_as):
    admin = make_user("admin@test.kz", role="admin", full_name="Admin")
    teacher = make_user("teacher@test.kz", role="teacher", full_name="Teacher")
    auth_as(admin)

    res_list = client.get("/api/users")
    assert res_list.status_code == 200
    assert len(res_list.json()) == 2

    res_one = client.get(f"/api/users/{teacher.id}")
    assert res_one.status_code == 200
    assert res_one.json()["email"] == "teacher@test.kz"

    res_patch = client.patch(
        f"/api/users/{teacher.id}",
        json={"full_name": "Senior Teacher", "role": "student"},
    )
    assert res_patch.status_code == 200
    assert res_patch.json()["full_name"] == "Senior Teacher"
    assert res_patch.json()["role"] == "student"

    res_del = client.delete(f"/api/users/{teacher.id}")
    assert res_del.status_code == 204
    assert client.get(f"/api/users/{teacher.id}").status_code == 404


def test_users_permissions_and_self_protection(client, make_user, auth_as):
    admin = make_user("admin@test.kz", role="admin")
    teacher = make_user("teacher@test.kz", role="teacher")
    student = make_user("student@test.kz", role="student")

    auth_as(teacher)
    assert client.get("/api/users").status_code == 403

    auth_as(student)
    assert client.get("/api/users").status_code == 403

    auth_as(admin)
    assert client.get("/api/users/9999").status_code == 404
    assert (
        client.patch(f"/api/users/{admin.id}", json={"role": "student"}).status_code
        == 400
    )
    assert client.delete(f"/api/users/{admin.id}").status_code == 400
