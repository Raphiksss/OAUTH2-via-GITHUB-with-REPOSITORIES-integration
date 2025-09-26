from fastapi import FastAPI
from app.config import settings
from starlette.middleware.sessions import SessionMiddleware
from routes.auth import router
import uvicorn
app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    same_site="lax",
    https_only=False,
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port = 8000, reload = True)