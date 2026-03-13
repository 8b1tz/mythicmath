# MythicMath Backend

Guia rapido para o time de front rodar o backend **com Docker** ou **com venv**.

## Requisitos
- Docker Desktop (opcao 1)
- OU Python 3.8+ (opcao 2)

---

## Opcao 1: Rodar com Docker (API + Postgres + Redis)

```powershell
cd C:\Users\user\Downloads\mythicmath\backend
docker compose up -d
docker compose run --rm api alembic upgrade head
```

Pronto. A API fica em `http://127.0.0.1:8000`.

Abrir:
- Docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`
- WebSocket: `ws://127.0.0.1:8000/ws`

---

## Opcao 2: Rodar com venv (SQLite local)

```powershell
cd C:\Users\user\Downloads\mythicmath\backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt

$env:DATABASE_URL="sqlite+aiosqlite:///./dev.db"
.\.venv\Scripts\alembic.exe upgrade head

$env:DATABASE_URL="sqlite+aiosqlite:///./dev.db"
.\.venv\Scripts\uvicorn app.main:app --reload
```

Pronto. A API fica em `http://127.0.0.1:8000`.

---

## Endpoints principais

### Register
`POST /register`

Body:
```json
{ "name": "Ana", "email": "ana@email.com", "password": "123456" }
```

Response:
```json
{ "id": 1, "name": "Ana", "email": "ana@email.com", "token": "..." }
```

### Login
`POST /login`

Body (identifier = email OU username):
```json
{ "identifier": "ana@email.com", "password": "123456" }
```
ou
```json
{ "identifier": "Ana", "password": "123456" }
```

Response:
```json
{ "id": 1, "name": "Ana", "email": "ana@email.com", "token": "..." }
```

---

## Observacao
- Docker usa o `.env` local automaticamente.
- venv usa SQLite (`dev.db`) e nao precisa de Postgres/Redis.
