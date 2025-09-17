from app.routes.auth import router as github_router
from starlette.middleware.sessions import SessionMiddleware
from fastapi import FastAPI
from app.config import settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

app.include_router(github_router)