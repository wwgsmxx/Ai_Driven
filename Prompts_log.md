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

### 8-сабақ · Тексеру нәтижелері (psql шектеулері және миграция)
- **Миграция тексеруінің 6 жауабы:** 1) 4 кесте (`users`, `quizzes`, `attempts`, `questions`); 2) `password` жоқ; 3) 4 FK (`ON DELETE CASCADE`); 4) UNIQUE (`ix_users_email`) және CHECK (`ck_users_role`, `ck_questions_source`, `ck_questions_correct_index`, `ck_attempts_score`, `ck_attempts_total`); 5) `downgrade()` кері ретпен жояды; 6) `alembic upgrade head --sql` валидацияланды.
- **Бұзылған 3 шектеу (psql тексеруі):**
  1. `UNIQUE` (`ix_users_email`): бірдей `email` екінші рет қосылғанда `duplicate key value violates unique constraint "ix_users_email"` қатесі.
  2. `CHECK` (`ck_users_role`): `role = 'boss'` берілгенде `violates check constraint "ck_users_role"` қатесі.
  3. `FOREIGN KEY` (`quizzes_owner_id_fkey`): жоқ `owner_id = 999` берілгенде `violates foreign key constraint` қатесі.

<!-- Шешім белгілері: ✅ қабылданды · ✏️ өзгертілді · ❌ қабылданбады -->
