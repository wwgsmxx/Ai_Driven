# API жобасы (6–10-сабақтар)

| Әдіс | Жол | Кім | Не істейді | Story | Кесте |
|---|---|---|---|---|---|
| `GET` | `/api/auth/me` | `student, teacher, admin` | Кіріп тұрған пайдаланушының профилі мен рөлі | — | `users` |
| `POST` | `/api/quizzes` | `teacher, admin` | Жаңа тест құру | US-1 | `quizzes` |
| `POST` | `/api/quizzes/{id}/questions` | `teacher, admin` | Тестке сұрақ қосу | US-1 | `questions` |
| `POST` | `/api/quizzes/{id}/publish` | `teacher, admin` | Тестті жариялау (`is_published=true`) | US-2 | `quizzes` |
| `POST` | `/api/quizzes/{id}/attempts` | `student` | Тест тапсыру және ұпай есептеу | US-3 | `attempts` |
| `POST` | `/api/ai/generate-questions` | `teacher, admin` | AI (LLM) арқылы сұрақтар ұсынысын генерациялау | US-4 | `—` (сақтау US-1 арқылы) |
| `GET` | `/api/attempts/me` | `student` | Менің тест тапсыру нәтижелерім | US-5 | `attempts` |
| `GET` | `/api/quizzes` | `student, teacher, admin` | Тесттер тізімі (студент — жарияланғандар, мұғалім — өзінікі + жарияланғандар) | US-6 | `quizzes` |
| `GET` | `/api/quizzes/{id}` | `student, teacher, admin` | Тест пен сұрақтарды ашып қарау | US-1, US-3 | `quizzes, questions` |
| `PATCH` | `/api/quizzes/{id}` | `teacher (иесі), admin` | Тест мәліметтерін түзету | US-6 | `quizzes` |
| `DELETE` | `/api/quizzes/{id}` | `teacher (иесі), admin` | Тестті өшіру | US-6 | `quizzes` |
| `GET` | `/api/users` | `admin` | Пайдаланушылар тізімі | — | `users` |
| `GET` | `/api/users/{id}` | `admin` | Бір пайдаланушы профилі | — | `users` |
| `DELETE` | `/api/users/{id}` | `admin` | Пайдаланушыны өшіру (өзін өшіре алмайды → `400`) | — | `users` |

---

## Рөл матрицасы (10-сабақ · Keycloak RBAC)

| Endpoint | Токенсіз | `student` | `teacher` (өзінікі) | `teacher` (бөтен) | `admin` |
|---|---|---|---|---|---|
| `GET /api/health` | `200` | `200` | `200` | `200` | `200` |
| `GET /api/auth/me` | `401` | `200` | `200` | `200` | `200` |
| `GET /api/quizzes` | `401` | `200` | `200` | `200` | `200` |
| `POST /api/quizzes` | `401` | `403` | `201` | `201` | `201` |
| `PATCH /api/quizzes/{id}` | `401` | `403` | `200` | `403` | `200` |
| `DELETE /api/quizzes/{id}` | `401` | `403` | `204` | `403` | `204` |
| `POST /api/quizzes/{id}/questions` | `401` | `403` | `201` | `403` | `201` |
| `PATCH /api/questions/{id}` | `401` | `403` | `200` | `403` | `200` |
| `DELETE /api/questions/{id}` | `401` | `403` | `204` | `403` | `204` |
| `POST /api/quizzes/{id}/publish` | `401` | `403` | `200` | `403` | `200` |
| `POST /api/quizzes/{id}/attempts` | `401` | `201` | `403` | `403` | `403` |
| `GET /api/attempts/me` | `401` | `200` | `403` | `403` | `403` |
| `GET /api/users` | `401` | `403` | `403` | `403` | `200` |
| `GET /api/users/{id}` | `401` | `403` | `403` | `403` | `200` |
| `DELETE /api/users/{id}` | `401` | `403` | `403` | `403` | `204` (өзін → `400`) |

---

## Жауап кодтары («Сервер не дейді?»)

| Код | Қарапайым тілмен | Мысал |
|---|---|---|
| **200** | Бәрі дұрыс | Тесттер тізімі немесе нәтиже қайтты (`GET`, `PATCH`) |
| **201** | Құрылды | Жаңа тест немесе сұрақ құрылды (`POST`) |
| **204** | Өшірілді, қайтаратын ештеңе жоқ | Тест өшірілді (`DELETE`) |
| **400** | Ереже бұзылды | Сұрақсыз тестті жариялауға тырысты |
| **401** | Сіз кірмегенсіз | Сұраныста токен жоқ, мерзімі өткен немесе қолтаңбасы жарамсыз |
| **403** | Кірдіңіз, бірақ рұқсат жоқ | Студент тест құрғысы немесе жариялағысы келеді |
| **404** | Табылмады | Мұндай ID-мен тест немесе сұрақ жоқ |
| **422** | Дерек пішімі қате | Тест атауы 2 таңбадан қысқа немесе сұрақ пішіні қате |
| **503** | Сыртқы сервис қолжетімді емес | Keycloak JWKS кілтін алу мүмкін емес |

---

## Сәйкестік: story → endpoint → кесте

| Story | Endpoint | Кесте |
|---|---|---|
| **US-1** (тест құру, сұрақ қосу) | `POST /api/quizzes`, `POST /api/quizzes/{id}/questions` | `quizzes`, `questions` |
| **US-2** (жариялау) | `POST /api/quizzes/{id}/publish` | `quizzes` |
| **US-3** (тапсыру, ұпай) | `POST /api/quizzes/{id}/attempts` | `attempts` |
| **US-4** (AI ұсынысы) | `POST /api/ai/generate-questions` | `—` (сақтау US-1 арқылы) |
| **US-5** (нәтижелерім) | `GET /api/attempts/me` | `attempts` |
| **US-6** (өз тесттерім) | `GET /api/quizzes` | `quizzes` |
