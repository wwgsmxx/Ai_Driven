def test_users_admin_list_get_delete(client, make_user, auth_as):
    admin = make_user("admin@test.kz", role="admin", full_name="Admin")
    teacher = make_user("teacher@test.kz", role="teacher", full_name="Teacher")
    auth_as(admin)

    res_list = client.get("/api/users")
    assert res_list.status_code == 200
    assert len(res_list.json()) == 2
    assert "password" not in res_list.text

    res_one = client.get(f"/api/users/{teacher.id}")
    assert res_one.status_code == 200
    assert res_one.json()["email"] == "teacher@test.kz"

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
    assert client.delete(f"/api/users/{admin.id}").status_code == 400
