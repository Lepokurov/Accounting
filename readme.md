# Accounting API (FastAPI)

## Quick start — Option A: Poetry (recommended)
1. Create `.env` from `.env.example`.
2. Install Poetry, then:
   ```bash
   poetry install
   poetry run alembic revision -m "init" --autogenerate
   poetry run alembic upgrade head
   poetry run uvicorn app.main:app --reload
   ```
3. Swagger: http://localhost:8000/docs

## Quick start — Option B: pip + requirements.txt (староверы)
1. Create and fill `.env` from `.env.example`.
2. Create venv and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run migrations (uses `SYNC_DATABASE_URL` from `.env`):
   ```bash
   alembic revision -m "init" --autogenerate
   alembic upgrade head
   ```
4. Launch app:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Swagger: http://localhost:8000/docs

## Auth
Send header: `Authorization: Bearer <token>`

## Endpoints
- `GET/POST/PATCH/DELETE /users`
- `GET/POST/PATCH/DELETE /executors`
- `GET/POST/PATCH/DELETE /managers`
- `GET/POST/PATCH/DELETE /entries`
  - Filters: `user_id`, `executor_id`, `manager_id`, `date_from`, `date_to`, `status`
  - Pagination: `limit` (default 50), `offset`

## Notes
- `amount` is non-negative; business sign inferred from `status` (`cancelled/rejected` etc.).
- Status enum: `draft | pending | approved | paid | cancelled | rejected`.
- Soft delete via `deleted_at`; queries exclude deleted rows.
- Designed for future M2M managers/executors per entry via linking tables.
