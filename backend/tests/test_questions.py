from app.models.quiz import Quiz


def test_questions_crud_and_rules(client, db, make_user, auth_as):
    teacher1 = make_user("t1@test.kz", role="teacher")
    teacher2 = make_user("t2@test.kz", role="teacher")

    draft = Quiz(title="Python", topic="IT", owner_id=teacher1.id, is_published=False)
    pub = Quiz(title="Java", topic="IT", owner_id=teacher1.id, is_published=True)
    db.add_all([draft, pub])
    db.commit()

    auth_as(teacher1)
    # Дұрыс сұрақ қосу -> 201
    res = client.post(
        f"/api/quizzes/{draft.id}/questions",
        json={
            "text": "2 + 2 неше?",
            "options": ["3", "4", "5"],
            "correct_index": 1,
        },
    )
    assert res.status_code == 201
    q_id = res.json()["id"]

    # correct_index > нұсқа саны -> 400
    assert (
        client.post(
            f"/api/quizzes/{draft.id}/questions",
            json={
                "text": "Қате индекс",
                "options": ["A", "B"],
                "correct_index": 5,
            },
        ).status_code
        == 400
    )

    # Жарияланған тестке қосуға болмайды -> 400
    assert (
        client.post(
            f"/api/quizzes/{pub.id}/questions",
            json={
                "text": "Жарияланған тестке",
                "options": ["A", "B"],
                "correct_index": 0,
            },
        ).status_code
        == 400
    )

    # Сұрақты өзгерту -> 200
    upd = client.patch(f"/api/questions/{q_id}", json={"text": "2 * 2 неше?"})
    assert upd.status_code == 200
    assert upd.json()["text"] == "2 * 2 неше?"

    # Бөтен мұғалім өзгерте/өшіре алмайды -> 403
    auth_as(teacher2)
    res_upd = client.patch(f"/api/questions/{q_id}", json={"text": "Hack"})
    assert res_upd.status_code == 403
    assert client.delete(f"/api/questions/{q_id}").status_code == 403

    # Иесі өшіреді -> 204
    auth_as(teacher1)
    assert client.delete(f"/api/questions/{q_id}").status_code == 204
    assert (
        client.patch(f"/api/questions/{q_id}", json={"text": "Updated"}).status_code
        == 404
    )

