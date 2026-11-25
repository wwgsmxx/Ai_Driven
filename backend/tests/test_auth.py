def test_register_and_login_flow(client):
    # 1. Сәтті тіркелу -> 201, пароль жауапта жоқ, рөл student
    res = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "strongpassword123",
            "full_name": "Жаңа Студент",
        },
    )
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "newuser@example.com"
    assert body["role"] == "student"
    assert "password" not in body
    assert "password_hash" not in body

    # 2. Қайталанатын email -> 409
    dup = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "anotherpassword",
        },
    )
    assert dup.status_code == 409

    # 3. Қысқа пароль -> 422
    short_pw = client.post(
        "/api/auth/register",
        json={"email": "short@example.com", "password": "123"},
    )
    assert short_pw.status_code == 422

    # 4. Тіркелуде role: admin (mass assignment) -> 422
    mass_assign = client.post(
        "/api/auth/register",
        json={
            "email": "hacker@example.com",
            "password": "strongpassword123",
            "role": "admin",
        },
    )
    assert mass_assign.status_code == 422

    # 5. Сәтті кіру тексерісі -> 200, токен берілмейді
    login_ok = client.post(
        "/api/auth/login",
        json={"email": "newuser@example.com", "password": "strongpassword123"},
    )
    assert login_ok.status_code == 200
    login_body = login_ok.json()
    assert login_body["user"]["email"] == "newuser@example.com"
    assert "access_token" not in login_body
    assert "token" not in login_body

    # 6. Қате пароль немесе жоқ email -> 401
    login_bad_pw = client.post(
        "/api/auth/login",
        json={"email": "newuser@example.com", "password": "wrongpassword"},
    )
    assert login_bad_pw.status_code == 401
    assert login_bad_pw.json()["detail"] == "Email немесе құпиясөз қате"

    login_no_user = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "strongpassword123"},
    )
    assert login_no_user.status_code == 401
    assert login_no_user.json()["detail"] == "Email немесе құпиясөз қате"
