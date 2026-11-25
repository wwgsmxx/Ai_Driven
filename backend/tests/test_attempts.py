from app.models.question import Question
from app.models.quiz import Quiz


def test_publish_and_attempts_flow(client, db, make_user, auth_as):
    teacher = make_user("t@test.kz", role="teacher")
    student = make_user("s@test.kz", role="student")

    quiz = Quiz(
        title="Тарих",
        topic="Қазақстан",
        owner_id=teacher.id,
        is_published=False,
    )
    db.add(quiz)
    db.commit()

    auth_as(teacher)
    # Сұрақсыз тестті жариялауға болмайды -> 400
    assert client.post(f"/api/quizzes/{quiz.id}/publish").status_code == 400

    # 2 сұрақ қосамыз
    db.add_all(
        [
            Question(
                quiz_id=quiz.id,
                position=1,
                text="1-сұрақ",
                options=["A", "B"],
                correct_index=0,
            ),
            Question(
                quiz_id=quiz.id,
                position=2,
                text="2-сұрақ",
                options=["C", "D"],
                correct_index=1,
            ),
        ]
    )
    db.commit()

    # Жариялау -> 200
    pub_res = client.post(f"/api/quizzes/{quiz.id}/publish")
    assert pub_res.status_code == 200
    assert pub_res.json()["is_published"] is True

    # Мұғалім тест тапсыра алмайды -> 403
    res_forbidden = client.post(
        f"/api/quizzes/{quiz.id}/attempts", json={"answers": [0, 1]}
    )
    assert res_forbidden.status_code == 403

    # Студент жауап саны қате болса -> 400
    auth_as(student)
    res_bad = client.post(f"/api/quizzes/{quiz.id}/attempts", json={"answers": [0]})
    assert res_bad.status_code == 400

    # Дұрыс тапсыру -> 201 (1 дұрыс, 1 қате = score 1, total 2)
    att = client.post(f"/api/quizzes/{quiz.id}/attempts", json={"answers": [0, 0]})
    assert att.status_code == 201
    assert att.json()["score"] == 1
    assert att.json()["total"] == 2

    # Менің нәтижелерім -> 200
    my_res = client.get("/api/attempts/me")
    assert my_res.status_code == 200
    assert len(my_res.json()) == 1
    assert my_res.json()[0]["score"] == 1

