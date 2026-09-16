# Bellbird Books — Inventory & Order Management System

A lightweight internal web application for **Bellbird Books**, an independent
second-hand bookshop at 118 Fernbrook Road, Ashgrove, Brisbane. The system
replaces paper ledgers and scattered spreadsheets for:

- Stock keeping for ~4,200 new titles (quantity-tracked) and ~2,500
  second-hand copies (each copy recorded individually).
- Customer record keeping and order tracking with four states:
  `placed`, `arrived`, `collected`, `cancelled`.
- Counter-facing search by title, author and shelf location.
- Basic dashboard: live stock levels and pending order queue.

## Tech stack

- Python 3.11+ / Flask 3
- SQLAlchemy ORM (SQLite in development, Postgres in production)
- Server-rendered HTML + vanilla CSS/JS (no frontend framework)

## Local setup

```bash
python -m venv venv
# Windows:  venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # then edit SECRET_KEY
flask --app app --debug run
```

Open http://127.0.0.1:5000.

## Repository layout

```
bellbird-books/
├── app.py              # application factory + entry point
├── config.py           # per-environment configuration
├── models.py           # SQLAlchemy models
├── seed.py             # demo data loader
├── blueprints/         # route modules, one per domain
├── templates/          # Jinja2 templates
├── static/             # CSS / JS
├── Procfile            # production web process
└── render.yaml         # one-click deploy configuration
```

## Branching model

See `docs/configuration-management.md` (project report) for the full
branching strategy. In short:

- `main` — always deployable, tagged releases only.
- `feature/*` — short-lived branches off `main`, merged via pull request.
