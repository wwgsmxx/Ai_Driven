# QuizAI — AI агенттерге арналған жоба ережелері

Antigravity бұл файлды әр сұраныста оқиды. Студенттер өз жобасына осы үлгіні бейімдейді.

## Жоба
Мұғалімдерге арналған AI тест генераторы. Стек: FastAPI (backend/), PostgreSQL + SQLAlchemy 2 + Alembic,

- Токенді тексеру: тек RS256, `iss`, `aud`, `exp` міндетті (`core/security.py`). Рөл — `realm_access.roles`-тан, клиент жіберген өрістен емес.
- SQL-ді жолдармен (f-string) құрастырма — тек SQLAlchemy/параметрлер.
- Тіркелуде рөлді клиенттен қабылдама (mass assignment).
- LLM жауабына сенбе: әрдайым Pydantic арқылы тексер, қате болса fallback.
- `docker compose down -v`, `DROP`, `rm -rf`, `git push --force` — сұрамай орындама.

## Prompt log
Маңызды AI әрекеттесуден кейін `docs/prompt-log.md`-ға жазба қосуды ұсын (skill: `prompt-log`).