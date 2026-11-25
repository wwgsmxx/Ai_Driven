from app.models.question import Question
from app.models.quiz import Quiz


def test_quizzes_crud_and_visibility(client, db, make_user, auth_as):
    teacher1 = make_user("t1@test.kz", role="teacher")
    teacher2 = make_user("t2@test.kz", role="teacher")
    student = make_user("s1@test.kz", role="student")
    admin = make_user("a1@test.kz", role="admin")

    # 401: база бос кезде демо-пайдаланушы табылмайды
    assert client.get("/api/quizzes").status_code == 401

    # Teacher 1 тест құрады
    auth_as(teacher1)
    res = client.post("/api/quizzes", json={"title": "Алгебра", "topic": "Математика"})
    assert res.status_code == 201
    q1_id = res.json()["id"]

    # Validation 422: қысқа атау
    assert client.post("/api/quizzes", json={"title": "А"}).status_code == 422

    # Teacher 2 жарияланған тест құрады
    q2 = Quiz(title="Физика", topic="Механика", owner_id=teacher2.id, is_published=True)
    db.add(q2)
    db.flush()
    db.add(
        Question(
            quiz_id=q2.id,
            position=1,
            text="Күш өлшем бірлігі?",
            options=["Джоуль", "Ньютон", "Ватт"],
            correct_index=1,
        )
    )
    db.commit()

    # Student тек жарияланған тестті көреді және correct_index алмайды
    auth_as(student)
    res_s = client.post("/api/quizzes", json={"title": "Student Quiz"})
    assert res_s.status_code == 403
    list_s = client.get("/api/quizzes")
    assert list_s.status_code == 200
    assert [q["id"] for q in list_s.json()] == [q2.id]

    detail_s = client.get(f"/api/quizzes/{q2.id}")
    assert detail_s.status_code == 200
    assert "correct_index" not in detail_s.json()["questions"][0]

    # Teacher 1 өз тестін + жарияланғандарды көреді
    auth_as(teacher1)
    assert len(client.get("/api/quizzes").json()) == 2
    res_f = client.patch(f"/api/quizzes/{q2.id}", json={"title": "New"})
    assert res_f.status_code == 403
    assert client.delete(f"/api/quizzes/{q2.id}").status_code == 403

    # Teacher 1 өз тестін өңдейді және өшіреді
    upd = client.patch(f"/api/quizzes/{q1_id}", json={"title": "Геометрия"})
    assert upd.status_code == 200
    assert upd.json()["title"] == "Геометрия"
    assert client.delete(f"/api/quizzes/{q1_id}").status_code == 204
    assert client.get(f"/api/quizzes/{q1_id}").status_code == 404

    # Admin бәрін көреді
    auth_as(admin)
    assert len(client.get("/api/quizzes").json()) == 1
