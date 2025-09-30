# Database Initialization Guide (PostgreSQL)

## 1. Create user and database
```sql
-- connect as superuser (usually postgres)
psql -U postgres -h localhost

-- create user with password
CREATE USER acc WITH PASSWORD 'accpass';

-- create database owned by user
CREATE DATABASE accounting OWNER acc;

-- grant privileges
GRANT ALL PRIVILEGES ON DATABASE accounting TO acc;
```

## 2. Grant privileges on schema/tables
After applying migrations:
```sql
\c accounting
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO acc;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO acc;
```
Make privileges default for new tables/sequences:
```sql
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO acc;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO acc;
```

## 3. Configure `.env`
```ini
DATABASE_URL=postgresql+asyncpg://acc:accpass@localhost:5432/accounting
SYNC_DATABASE_URL=postgresql+psycopg2://acc:accpass@localhost:5432/accounting
API_TOKEN=supersecrettoken
APP_ENV=dev
```

## 4. Run migrations
If this is the **first time**, you need to create an initial revision and apply it:
```bash
alembic revision -m "init" --autogenerate
alembic upgrade head
```

If you have **already created the first migration file** (revision exists in `migrations/versions/`), then you only need to apply it:
```bash
alembic upgrade head
```

## 5. Verify connection
```bash
psql "postgresql://acc:accpass@localhost:5432/accounting" -c "\dt"
```
You should see the tables `users`, `executors`, `managers`, `entries`.
