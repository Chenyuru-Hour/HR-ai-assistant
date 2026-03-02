# Backend Quick Start

## 1. Install dependencies

```bash
cd backend
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Configure environment

```bash
copy .env.example .env
```

Set `LLM_API_KEY` in `.env` before integrating model calls.

## 3. Run server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 4. Run tests

```bash
pytest
```

## Available routes

- `GET /api/v1/health`
- `GET /api/v1/resume/ping`
- `GET /api/v1/parse/ping`
- `GET /api/v1/score/ping`
