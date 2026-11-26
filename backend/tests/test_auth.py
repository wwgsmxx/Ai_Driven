def test_register_and_login_flow(client):
    # 1. Сәтті тіркелу (teacher рөлімен) -> 201, пароль жауапта жоқ
    res = client.post(
        "/api/auth/register",
        json={
            "email": "aru@example.com",
            "full_name": "Ару Сәрсен",
            "password": "qwerty-123",
            "role": "teacher",
        },
    )
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "aru@example.com"
    assert body["role"] == "teacher"
    assert "password" not in body
    assert "password_hash" not in body

    # 2. Қайталанатын email -> 409
    dup = client.post(
        "/api/auth/register",
        json={
            "email": "aru@example.com",
            "full_name": "Ару Сәрсен",
            "password": "qwerty-123",
            "role": "teacher",
        },
    )
    assert dup.status_code == 409

    # 3. Қысқа пароль (< 8) -> 422
    short_pw = client.post(
        "/api/auth/register",
        json={"email": "short@example.com", "full_name": "Ару", "password": "123"},
    )
    assert short_pw.status_code == 422

    # 4. Тіркелуде role: admin -> 422
    mass_assign = client.post(
        "/api/auth/register",
        json={
            "email": "hacker@example.com",
            "full_name": "Хакер",
            "password": "qwerty-123",
            "role": "admin",
        },
    )
    assert mass_assign.status_code == 422

    # 5. Сәтті кіру тексерісі -> 200, UserRead қайтарады (токен жоқ)
    login_ok = client.post(
        "/api/auth/login",
        json={"email": "aru@example.com", "password": "qwerty-123"},
    )
    assert login_ok.status_code == 200
    login_body = login_ok.json()
    assert login_body["email"] == "aru@example.com"
    assert "password" not in login_body
    assert "password_hash" not in login_body

    # 6. Қате пароль немесе жоқ email -> 401
    login_bad_pw = client.post(
        "/api/auth/login",
        json={"email": "aru@example.com", "password": "wrong-pass"},
    )
    assert login_bad_pw.status_code == 401
    assert login_bad_pw.json()["detail"] == "Email немесе құпиясөз қате"

    login_no_user = client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "qwerty-123"},
    )
    assert login_no_user.status_code == 401
    assert login_no_user.json()["detail"] == "Email немесе құпиясөз қате"
