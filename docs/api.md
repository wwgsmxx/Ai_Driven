# API жобасы (6-сабақ)

| Әдіс | Жол | Кім | Не істейді | Story | Кесте |
|---|---|---|---|---|---|
| `POST` | `/api/quizzes` | `teacher` | Жаңа тест құру | US-1 | `quizzes` |
| `POST` | `/api/quizzes/{id}/questions` | `teacher` | Тестке сұрақ қосу | US-1 | `questions` |
| `POST` | `/api/quizzes/{id}/publish` | `teacher` | Тестті жариялау (`is_published=true`) | US-2 | `quizzes` |
| `POST` | `/api/quizzes/{id}/attempts` | `student` | Тест тапсыру және ұпай есептеу | US-3 | `attempts` |
| `POST` | `/api/ai/generate-questions` | `teacher` | AI (LLM) арқылы сұрақтар ұсынысын генерациялау | US-4 | `—` (сақтау US-1 арқылы) |
| `GET` | `/api/attempts/me` | `student` | Менің тест тапсыру нәтижелерім | US-5 | `attempts` |
| `GET` | `/api/quizzes` | `teacher` | Мұғалімнің өз тесттерінің тізімі | US-6 | `quizzes` |
| `GET` | `/api/quizzes/{id}` | `teacher, student` | Тест пен сұрақтарды ашып қарау | US-1, US-3 | `quizzes, questions` |
| `PATCH` | `/api/quizzes/{id}` | `teacher` | Тест мәліметтерін түзету | US-6 | `quizzes` |
| `DELETE` | `/api/quizzes/{id}` | `teacher` | Тестті өшіру | US-6 | `quizzes` |

---

## Жауап кодтары («Сервер не дейді?»)

| Код | Қарапайым тілмен | Мысал |
|---|---|---|
| **200** | Бәрі дұрыс | Тесттер тізімі немесе нәтиже қайтты (`GET`, `PATCH`) |
| **201** | Құрылды | Жаңа тест немесе сұрақ құрылды (`POST`) |
| **204** | Өшірілді, қайтаратын ештеңе жоқ | Тест өшірілді (`DELETE`) |
| **400** | Ереже бұзылды | Сұрақсыз тестті жариялауға тырысты |
| **401** | Сіз кірмегенсіз | Сұраныста токен жоқ |
| **403** | Кірдіңіз, бірақ рұқсат жоқ | Студент тест құрғысы немесе жариялағысы келеді |
| **404** | Табылмады | Мұндай ID-мен тест немесе сұрақ жоқ |
| **422** | Дерек пішімі қате | Тест атауы 2 таңбадан қысқа немесе сұрақ пішіні қате |

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
