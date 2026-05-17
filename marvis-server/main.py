from fastapi import FastAPI

from auth.v1.router import router as auth_router

app = FastAPI(title="Marvis", version="1.0.0")

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
