from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.routers import users, executors, managers, entries

app = FastAPI(
    title="Accounting API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Users", "description": "CRUD for users"},
        {"name": "Executors", "description": "CRUD for executors"},
        {"name": "Managers", "description": "CRUD for managers"},
        {"name": "Entries", "description": "Accounting entries with filters"},
    ],
)

app.include_router(users.router)
app.include_router(executors.router)
app.include_router(managers.router)
app.include_router(entries.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")