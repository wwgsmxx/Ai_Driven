from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.user import User

DEMO_USERS = [
    {"email": "teacher@demo.kz", "full_name": "Demo Teacher", "role": "teacher"},
    {"email": "student@demo.kz", "full_name": "Demo Student", "role": "student"},
    {"email": "admin@demo.kz", "full_name": "Demo Admin", "role": "admin"},
]

DEMO_QUESTIONS = [
    {
        "position": 1,
        "text": "Python тілінде тізім (list) қай жақшамен жазылады?",
        "options": ["{}", "[]", "()", "<>"],
        "correct_index": 1,
    },
    {
        "position": 2,
        "text": "Python-да функция жариялау үшін қай кілт сөз қолданылады?",
        "options": ["func", "function", "def", "lambda"],
        "correct_index": 2,
    },
]


def seed() -> None:
    with SessionLocal() as db:
        users_by_email: dict[str, User] = {}
        for item in DEMO_USERS:
            user = db.scalar(select(User).where(User.email == item["email"]))
            if user is None:
                user = User(
                    email=item["email"],
                    full_name=item["full_name"],
                    role=item["role"],
                )
                db.add(user)
                db.flush()
            users_by_email[item["email"]] = user

        teacher = users_by_email["teacher@demo.kz"]
        quiz = db.scalar(
            select(Quiz).where(
                Quiz.owner_id == teacher.id,
                Quiz.title == "Python негіздері",
            )
        )
        if quiz is None:
            quiz = Quiz(
                title="Python негіздері",
                topic="Бағдарламалау",
                owner_id=teacher.id,
                is_published=True,
            )
            db.add(quiz)
            db.flush()

        existing_questions = db.scalar(
            select(Question).where(Question.quiz_id == quiz.id)
        )
        if existing_questions is None:
            for q in DEMO_QUESTIONS:
                db.add(
                    Question(
                        quiz_id=quiz.id,
                        position=q["position"],
                        text=q["text"],
                        options=q["options"],
                        correct_index=q["correct_index"],
                        source="manual",
                    )
                )

        db.commit()


if __name__ == "__main__":
    seed()
    print("Seed деректері сәтті енгізілді!")
