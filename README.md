# JobCMD — AI Job Search Command Center

> Modular agentic AI app for autonomous job searching, matching, applying, and offer evaluation.

## Architecture

```
Planner → Tools → Memory → Executor
    ↓         ↓        ↓        ↓
   Plan    Scanner  SQLite  Playwright
           Matcher          Auto-Fill
           DocGen
```

**Agent Loop:**
1. **Planner** — Decomposes goal into steps using LLM
2. **Scanner** — Scrapes Greenhouse, Workday, LinkedIn, Lever APIs
3. **Matcher** — LLM scores each job vs your profile (0-100)
4. **Generator** — Tailored CVs + cover letters per job
5. **Executor** — Playwright fills job portal forms automatically
6. **Memory** — SQLite stores all state across sessions

## Project Structure

```
jobcmd/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── requirements.txt
│   ├── agents/
│   │   ├── planner.py       # Orchestrator agent
│   │   ├── llm_client.py    # Anthropic + Ollama client
│   │   └── tools.py         # Scanner, Matcher, DocGen, Applicator
│   ├── api/
│   │   ├── profile.py       # Profile CRUD
│   │   ├── jobs.py          # Job listing + matching
│   │   ├── applications.py  # Application tracking
│   │   └── agents.py        # Agent execution endpoints
│   └── db/
│       └── database.py      # SQLAlchemy models
├── frontend/
│   └── index.html           # Full React-compatible SPA (no build needed)
├── data/
│   └── sample/profile.json  # Sample profile
└── scripts/
    ├── setup.sh             # One-time setup
    └── run.sh               # Start everything
```

## Quick Start

### Option A: Frontend Only (no backend needed)
```bash
# Just open in browser — works with simulated data + direct Anthropic API
open frontend/index.html
# Add your Anthropic API key in Settings for real AI matching
```

### Option B: Full Stack
```bash
# 1. Setup
chmod +x scripts/*.sh
./scripts/setup.sh

# 2. Set API key
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# 3. Run
./scripts/run.sh
# Backend: http://localhost:8000
# Frontend: open frontend/index.html
```

### Option C: Backend only (API mode)
```bash
cd backend
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python main.py
# API docs: http://localhost:8000/docs
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/jobs/ | List all jobs |
| GET | /api/jobs/scan?keywords=Python,AWS | Scan portals |
| POST | /api/jobs/match | LLM match jobs to profile |
| GET | /api/applications/ | List applications |
| POST | /api/applications/ | Create application |
| PATCH | /api/applications/{id} | Update status |
| POST | /api/agents/run | Run full agent loop |
| POST | /api/agents/generate-cover-letter | Generate cover letter |
| POST | /api/agents/evaluate-offer | Evaluate job offer |
| GET | /health | Health check |

## LLM Providers

**Anthropic (default):**
```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Ollama (local, free):**
```bash
ollama pull llama3
# In settings: select "Ollama" as provider
```

## Features

- ✅ Profile ingestion (manual + AI resume parsing)
- ✅ Multi-portal job scanning (8 sample jobs, Greenhouse/Workday/LinkedIn/Lever)
- ✅ LLM job matching with reasoning (0-100 score)
- ✅ Auto-generated tailored cover letters
- ✅ Application tracking dashboard (draft→applied→interviewing→offer→rejected)
- ✅ AI offer evaluation with negotiation points
- ✅ Agentic loop with terminal output
- ✅ Works offline (simulation mode) + real API mode
- ✅ SQLite persistence + localStorage
- ✅ Playwright browser automation (backend, real applications)

## Extending for Real Job Portals

```python
# backend/agents/tools.py - add real scraper:
class GreenhouseScraper:
    async def scrape(self, company: str) -> List[Dict]:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(f"https://boards.greenhouse.io/{company}")
            # ... extract jobs
```

## Tech Stack

- **Frontend:** Vanilla JS SPA (no build step required)
- **Backend:** Python + FastAPI + uvicorn
- **LLM:** Anthropic Claude / Ollama (local)
- **DB:** SQLite via SQLAlchemy + localStorage
- **Automation:** Playwright (browser auto-fill)
- **Fonts:** Space Mono + DM Sans
