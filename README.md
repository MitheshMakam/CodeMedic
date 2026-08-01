# CodeMedic AI

AI-powered GitHub repository reviewer built for agentic coding workflows. Paste a public GitHub repository URL, inspect focused reviews, or run the complete **Improve Everything** pipeline.

## Architecture

- `frontend/` — React 19 + Vite dashboard with Tailwind and streaming progress UI.
- `backend/` — FastAPI API, repository ingestion, rule-based preflight checks, and OpenAI structured review generation.

## Local development

```bash
cp backend/.env.example backend/.env
cd backend && python -m venv .venv && .venv/Scripts/pip install -r requirements.txt
.venv/Scripts/uvicorn app.main:app --reload --port 8000

cd frontend && npm install && npm run dev
```

Set `VITE_API_URL=http://localhost:8000` in `frontend/.env` if needed. Without `OPENAI_API_KEY`, CodeMedic remains useful: it performs deterministic repository scanning and returns a clear notice that AI enrichment is unavailable.

## Deploy

Deploy `frontend` to Vercel (the included `vercel.json` rewrites API requests to the configured backend) and deploy `backend` to Render using `render.yaml`. Add `OPENAI_API_KEY`, `GITHUB_TOKEN` (optional), and `CORS_ORIGINS` in Render.

## API

`POST /analyze`, `/summary`, `/bugs`, `/security`, `/tests`, `/readme`, `/commit`, `/explain`, and `/improve` accept JSON bodies documented by FastAPI at `/docs`. `POST /improve` returns server-sent events for real-time pipeline updates.
