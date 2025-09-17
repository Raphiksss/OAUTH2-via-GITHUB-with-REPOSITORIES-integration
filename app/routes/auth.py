from fastapi import APIRouter
from starlette.requests import Request

from app.config import settings, github

router = APIRouter(prefix="/auth")

@router.get("/github")
async def github_login(request: Request):
    redirect_uri = settings.GITHUB_REDIRECT_URI

    return await github.authorize_redirect(request, redirect_uri)

@router.get("/github/callback")
async def github_callback(request: Request):
    token = await github.authorize_access_token(request)
    print(token)
    resp = await github.get('user', token=token)
    
    return resp.json()
