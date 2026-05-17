from contextlib import asynccontextmanager

from fastapi import FastAPI

from auth.v1.router import router as auth_router
from config.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Marvis", version="1.0.0", lifespan=lifespan)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
