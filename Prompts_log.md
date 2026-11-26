# Prompt log

Курс бойы жүргізілетін AI әрекеттесу журналы. Әр маңызды промпттан кейін бір жол қосыңыз.
Бұл журнал аралық бақылауда (15 ұпай) және жеке қорғауда (15 ұпай) бағаланады.

**Ереже:** құпия кілттер, парольдер, жеке деректер журналға да, AI чатқа да жазылмайды.

| № | Күні | Тапсырма | Құрал / модель | Промпт (қысқаша) | Нәтиже | Шешім | Себебі |
|---|------|----------|----------------|------------------|--------|-------|--------|
| 1 | 2026-11-02 | QuizAI-да AI функциясының спецификациясы | Antigravity · Gemini | «Мұғалімге арналған AI функциясының спецификациясын docs/ai-feature-spec.md үлгісімен жаса» | Агент timeout пен fallback-ты жазбады | ✏️ өзгертілді | Қателер жолын өзім қостым |
| 2 | 2026-11-09 | Backend қабат картасын түзету және Mermaid сызбасын қосу | Antigravity · Gemini | «@docs/layers.md әр ұяшықты тексер, Mermaid сызбасын қос, кестені түзет» | Mermaid flowchart қосылды, Router, Schema, Service, Repository және Model қабаттары архитектураға сай түзетілді | ✅ қабылданды | Қабаттардың жауапкершілігі мен AGENTS.md ережелері толық сәйкестендірілді |
| 3 | 2026-11-09 | Backend қаңқасын құру (app/ папкалары, config, requirements) | Antigravity · Gemini | «@AGENTS.md @docs/layers.md бойынша backend ҚАҢҚАСЫН жаса...» | core, routers, schemas, services, repositories, models пакеттері, config.py, .env.example, requirements және pyproject.toml құрылып, ruff-пен тексерілді | ✅ қабылданды | Талап бойынша endpoint, model, SQL, main.py жазылмай, таза қаңқа дайындалды |
| 4 | 2026-11-16 | П1: ER диаграммасын жобалау және тексеру (6-сабақ) | Antigravity · Gemini | «@docs/user-stories.md @docs/er-diagram.md — менің кестелер тізімім...» | Агент кестелер арасындағы FK-ларды дұрыстады, бірақ `users` ішіне `password` бағанын және бөлек `roles` кестесін ұсынды | ❌ қабылданбады | Қауіпсіздік ережесі бойынша кіру Keycloak-та болады, пароль кестеге жазылмайды және бір `role` бағаны жеткілікті |
| 5 | 2026-11-16 | П2: API маршруттарын жобалау (6-сабақ) | Antigravity · Gemini | «@docs/user-stories.md @docs/er-diagram.md @docs/api.md — менің API жобам...» | Агент жолдардан етістіктерді алып тастап, REST көпше түріне келтірді және толық жауап кодтарын ұсынды | ✅ қабылданды | Әр Must story-ге кемінде бір endpoint сәйкестендірілді, REST ережелері сақталды |
| 6 | 2026-11-16 | П3: Жүйе архитектурасын сынау (6-сабақ) | Antigravity · Gemini | «Архитектура ұсын — сосын сынаймыз...» | Агент микросервистерді, Kafka кезегін және бөлек кэштеу серверін қосуды ұсынды | ❌ қабылданбады | 1 адам, 8 апталық жоба үшін тым күрделі (қызыл белгі); сабақ эталонына сай монолит (FastAPI + PostgreSQL + Keycloak + Ollama) таңдалды |
| 7 | 2026-11-16 | П4: Төрт құжаттың сәйкестігін тексеру (6-сабақ) | Antigravity · Gemini | «@docs/user-stories.md @docs/er-diagram.md @docs/api.md @docs/architecture.md сәйкестігін тексер...» | Төрт файлдағы атаулар (`quizzes`, `questions`, `attempts`), рөлдер мен компоненттер толық сәйкестендірілді | ✅ қабылданды | Барлық Must story-лерде endpoint пен кесте бар, бос ұяшық жоқ |
| 8 | 2026-11-20 | П1: Дерекқор қабаты мен модельдер (8-сабақ) | Antigravity · Gemini | «@AGENTS.md @docs/er-diagram.md @docs/layers.md бойынша дерекқор қабатын жаса...» | `database.py` және `User`, `Quiz`, `Question`, `Attempt` модельдері жасалды; `psycopg2` орнына `psycopg` драйвері және `ck_users_role` атауы түзетілді | ✏️ өзгертілді | Пароль мен `keycloak_id` қосылмады, барлық FK `ondelete="CASCADE"`, CHECK шектеулері сақталды |
| 9 | 2026-11-23 | П2: 0001 миграциясын тексеру парағы (8-сабақ) | Antigravity · Gemini | «Миграцияны ER диаграммамен салыстыр (6 сұрақ)...» | 1) 4 кесте бар; 2) Артық баған (`password`) жоқ; 3) 4 FK бәрі CASCADE; 4) `ix_users_email` UNIQUE, `ck_users_role` т.б. CHECK бар; 5) `downgrade()` кері ретпен (`questions`→`attempts`→`quizzes`→`users`); 6) `--sql` сәтті тексерілді | ✅ қабылданды | Барлық 6 критерий орындалды; `alembic upgrade head --sql` арқылы SQL расталды |
| 10 | 2026-11-23 | П3: Health endpoint-ке ДҚ тексеруін және conftest.py қосу (8-сабақ) | Antigravity · Gemini | «/api/health дерекқорды да тексерсін...» | `HealthRead`-қа `services: dict[str, str]` қосылды, `SELECT 1` сәтті болса `ok`/`up`, қате болса `degraded`/`down` қайтарады; `tests/conftest.py` (`quizai_test`) қосылды | ✅ қабылданды | 500 қатесін бермейді, тесттер бөлек `quizai_test` базасында жүреді |
| 11 | 2026-11-23 | П1–П3: Негізгі объект (`quiz`) үшін Schema, Repository, Service, Router және Seed (9-сабақ) | Antigravity · Gemini | «Негізгі объектім quiz үшін schema, repository, service, errors.py, deps.py, seed.py және 5 CRUD endpoint жаса» | `QuizCreate`, `QuizUpdate`, `QuizRead`, `QuizRepository`, `QuizService`, `errors.py`, `deps.py`, `seed.py` және `routers/quizzes.py` құрылды | ✅ қабылданды | Router-де SQL жоқ, Service-те `HTTPException` жоқ, `update`-те `exclude_unset=True, exclude_none=True` қолданылды |
| 12 | 2026-11-26 | П4–П5: Тіркелу (`argon2`), 0002 миграция және пайдаланушыларды басқару (`admin`) (9-сабақ) | Antigravity · Gemini | «Тіркелу мен кіруді тексеруді жаса (pwdlib[argon2], UserRegister, UserLogin) және admin үшін /api/users CRUD қос» | `core/passwords.py` (`$argon2id$`), `0002` миграциясы (`password_hash`), `routers/auth.py` және `routers/users.py` жасалды | ✅ қабылданды | Дерекқорда тек `$argon2id$` хэш сақталады, `UserRead`-та пароль жоқ, өз рөлін өзгерту/өзін өшіру 400 қайтарады |
| 13 | 2026-11-26 | П6: Бағынышты объект (`question`) және негізгі әрекет (`publish`, `attempt`) + автотесттер (9-сабақ) | Antigravity · Gemini | «Бағынышты объект question және негізгі әрекет attempt үшін қабаттар мен автотесттерді жаса» | `questions.py`, `attempts.py` роутерлері/сервистері/репозиторийлері және `test_users.py`, `test_auth.py`, `test_quizzes.py`, `test_questions.py`, `test_attempts.py` жасалды | ✅ қабылданды | Жарияланған тестті өзгерту → 400, сұрақсыз жариялау → 400, бөтен тест → 403, студентке `correct_index` берілмейді |

### 8-сабақ · Тексеру нәтижелері (psql шектеулері және миграция)
- **Миграция тексеруінің 6 жауабы:** 1) 4 кесте (`users`, `quizzes`, `attempts`, `questions`); 2) `password` жоқ; 3) 4 FK (`ON DELETE CASCADE`); 4) UNIQUE (`ix_users_email`) және CHECK (`ck_users_role`, `ck_questions_source`, `ck_questions_correct_index`, `ck_attempts_score`, `ck_attempts_total`); 5) `downgrade()` кері ретпен жояды; 6) `alembic upgrade head --sql` валидацияланды.
- **Бұзылған 3 шектеу (psql тексеруі):**
  1. `UNIQUE` (`ix_users_email`): бірдей `email` екінші рет қосылғанда `duplicate key value violates unique constraint "ix_users_email"` қатесі.
  2. `CHECK` (`ck_users_role`): `role = 'boss'` берілгенде `violates check constraint "ck_users_role"` қатесі.
  3. `FOREIGN KEY` (`quizzes_owner_id_fkey`): жоқ `owner_id = 999` берілгенде `violates foreign key constraint` қатесі.

---

### 9-сабақ · Өз жобамызға аудару кестесі (QuizAI)
- **Рөлдер:** `student` · `teacher` · `admin`
- **Негізгі объект (`<объект>`):** тест (`quiz`)
- **Бағынышты объект (`<бағынышты>`):** сұрақ (`question`)
- **Негізгі әрекет (`<әрекет>`):** тестті жариялау (`publish`) және тапсыру (`attempt`)
- **«Менің ...»:** менің нәтижелерім (`GET /api/attempts/me`)
- **Бизнес-ереже → 400:** сұрақсыз тестті жариялау, жарияланған тесттің сұрағын өзгерту, `correct_index >= len(options)`, жауап санының сұрақ санына сәйкес келмеуі.

#### Тексеру парағы 1 — Негізгі объект (`quizzes`): 8 сұраныс
| № | Сұраныс | Не жібереміз | Күтеміз | Алынған код |
|---|---|---|---|---|
| 1 | `GET /api/quizzes` | — | `200`, тізім | **200** |
| 2 | `POST /api/quizzes` | `{"title": "Python негіздері", "topic": "Бағдарламалау"}` | `201`, жаңа `id` | **201** |
| 3 | `GET /api/quizzes/{id}` | 2-дегі `id` | `200` | **200** |
| 4 | `PATCH /api/quizzes/{id}` | `{"topic": "Python"}` | `200`, `title` өзгермеді | **200** |
| 5 | `POST /api/quizzes` | `{"title": "ab"}` | `422` | **422** |
| 6 | `GET /api/quizzes/9999` | — | `404` | **404** |
| 7 | `DELETE /api/quizzes/{id}` | 2-дегі `id` | `204` | **204** |
| 8 | `GET /api/quizzes/{id}` | сол `id` | `404` — шынымен өшті | **404** |

#### Тексеру парағы 2 — Пайдаланушылар (`auth`, `users`): 10 сұраныс
| № | Сұраныс | Не жібереміз / кім атынан | Күтеміз | Алынған код |
|---|---|---|---|---|
| 1 | `POST /api/auth/register` | `{"email": "aru@example.com", "full_name": "Ару Сәрсен", "password": "qwerty-123", "role": "teacher"}` | `201`, `password` жоқ | **201** |
| 2 | `POST /api/auth/register` | 1-дегі JSON тағы бір рет | `409` | **409** |
| 3 | `POST /api/auth/register` | `"password": "123"` | `422` | **422** |
| 4 | `POST /api/auth/register` | `"role": "admin"` | `422` | **422** |
| 5 | `POST /api/auth/login` | `{"email": "aru@example.com", "password": "qwerty-123"}` | `200` | **200** |
| 6 | `POST /api/auth/login` | `"password": "wrong-pass"` | `401` | **401** |
| 7 | `GET /api/users` | `DEMO_USER_EMAIL=teacher@demo.kz` | `403` | **403** |
| 8 | `GET /api/users` | `DEMO_USER_EMAIL=admin@demo.kz` | `200` | **200** |
| 9 | `PATCH /api/users/{id}` | `{"role": "student"}` (тіркелген пайдаланушы) | `200` | **200** |
| 10 | `DELETE /api/users/{id}` | `admin` өзін | `400` | **400** |

<!-- Шешім белгілері: ✅ қабылданды · ✏️ өзгертілді · ❌ қабылданбады -->
