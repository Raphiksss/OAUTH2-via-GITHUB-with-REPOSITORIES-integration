from fastapi import FastAPI
from app.config import settings
from starlette.middleware.sessions import SessionMiddleware
from app.routes import router
import uvicorn
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    same_site="lax",
    https_only=False,
)
app.include_router(router)

