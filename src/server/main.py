from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.database import init_db
from api.routes import vault_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Make sure database is initialized before server starts."""
    print("Starting server and preparing database")
    init_db()
    yield
    print("Stopping server")

app = FastAPI(
    title="Distributed Password Manager API", 
    lifespan=lifespan
)

app.include_router(vault_router)

@app.get("/")
def validate_at_root():
    return {
        "status": "ok", 
        "message": "Distributed Password Manager API"
    }