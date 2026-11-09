# QuizAI — AI агенттерге арналған жоба ережелері

Antigravity бұл файлды әр сұраныста оқиды. Студенттер өз жобасына осы үлгіні бейімдейді.

## Жоба
Мұғалімдерге арналған AI тест генераторы. Стек: FastAPI (backend/), PostgreSQL + SQLAlchemy 2 + Alembic,
Keycloak (OIDC: кіру, тіркелу, рөлдер student/teacher/admin),
жергілікті LLM — Ollama (app/llm/), pytest, Next.js 16 (web/), Nginx, Docker Compose.
Кеңейтілген: Redis кэш, RabbitMQ + worker.

## Қабаттар — бұзуға болмайды
- `routers/` — тек HTTP. SQL жоқ, бизнес-ереже жоқ. Рөлді `Depends(require_role(...))` арқылы тексереді.
- `schemas/` — Pydantic. Студентке арналған схемада дұрыс жауап (`correct_index`) БОЛМАЙДЫ.
- `services/` — бизнес-логика; `HTTPException` емес, `services/errors.py` қателерін көтереді.
- `repositories/` — тек SQLAlchemy сұраулары.
- `models/` — модель өзгерсе, ЖАҢА Alembic миграциясы міндетті (`alembic revision --autogenerate`, содан кейін қарап шығу).
- `llm/` — LLM клиенттері. Бизнес-логика `services/ai_service.py`-де.

## Жұмыс тәртібі
1. Код жазбас бұрын жоспар ұсын: қай файлдар өзгереді және неге.
2. Бір тапсырма — бір кішкентай коммит. Тармақ (branch) + pull request.
3. Жаңа кітапхана қоспас бұрын сұра; оның бар екенін және нұсқасын тексер.
4. Өзгерістен кейін: `cd backend && ruff check . && pytest -q`; frontend: `cd web && npm run lint`.
5. Жаңа endpoint → кемінде бір сәтті және бір қате (401/403/404/422) тест.
6. Тесттерде нақты LLM-ді шақырма: `LLM_PROVIDER=fake` немесе mock.
7. Түсіндірме — қазақ тілінде; код, атаулар — ағылшынша.

## Қауіпсіздік — қатаң
- Құпиялар (KEYCLOAK_ADMIN_PASSWORD, POSTGRES_PASSWORD, парольдер) тек `.env`-те. `.env`-ті оқыма, көрсетпе, өзгертпе; жаңа айнымалы → `.env.example`-ға бос мәнмен.
- Кіру/тіркелу/құпиясөз — тек Keycloak. API-ға login endpoint, құпиясөз бағанын немесе өз JWT жасауын ҚОСПА.
- Токенді тексеру: тек RS256, `iss`, `aud`, `exp` міндетті (`core/security.py`). Рөл — `realm_access.roles`-тан, клиент жіберген өрістен емес.
- SQL-ді жолдармен (f-string) құрастырма — тек SQLAlchemy/параметрлер.
- Тіркелуде рөлді клиенттен қабылдама (mass assignment).
- LLM жауабына сенбе: әрдайым Pydantic арқылы тексер, қате болса fallback.
- `docker compose down -v`, `DROP`, `rm -rf`, `git push --force` — сұрамай орындама.

## Prompt log
Маңызды AI әрекеттесуден кейін `docs/prompt-log.md`-ға жазба қосуды ұсын (skill: `prompt-log`).