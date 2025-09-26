from fastapi import APIRouter, Request, HTTPException, Query
from app.config import github, settings
import base64
router = APIRouter(prefix = "/auth")

req_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

@router.get("/github", summary = "Аутентификация по гитхаб")
async def github_login(request: Request):
    redirect_uri = settings.GITHUB_REDIRECT_URI
    return await github.authorize_redirect(request, redirect_uri)

@router.get("/github/callback", summary = "Гитхаб редирект")
async def github_callback(request: Request):
    token = await github.authorize_access_token(request)
    request.session["gh_token"] = token
    return {"status": "ok"}

#Что бы название и овнер возврощялись корректно

@router.get("/github/repo", summary = "Получение репозиториев пользователя")
async def github_user_repos(request: Request, limit: int|None = Query(None)):
    token = request.session.get("gh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized")
    if not limit:
        limit = 10

    resp = await github.get(
        "user/repos",
        token=token,
        params={"sort": "updated", "page":1, "per_page": limit},
        headers=req_headers,
    )
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    data = resp.json()
    return [{"id": r.get("id"), "name": r.get("name")} for r in data]

@router.get("/github/repo/{repo_name}/tree", summary = "Получить дерево файлов у репозитория")
async def github_repo_tree_by_id_only_tree(
    request: Request,
    repo_name: str,
    repo_owner:str,
    ref: str | None = Query(None)
,
):
    #ref = ветка репозитория
    token = request.session.get("gh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized")
    if not ref:
        ref = "main"

    tree_resp = await github.get(
        f"repos/{repo_owner}/{repo_name}/git/trees/{ref}",
        token=token,
        params={"recursive": 1},
        headers=req_headers,
    )

    if tree_resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Tree not found for given ref")
    if tree_resp.status_code >= 400:
        raise HTTPException(status_code=tree_resp.status_code, detail=tree_resp.text)

    tree_json = tree_resp.json()
    entries = tree_json.get("tree", [])

    tree = [
        {
            "path": e.get("path"),
        }
        for e in entries
    ]

    return {
        "owner": repo_owner,
        "repo": repo_name,
        "ref": ref,
        "tree": tree,
    }

#

@router.get("/github/repo/{repo_name}/file", summary = "Получить содержимое файла")
async def github_repo_file_content_by_id(
    request: Request,
    repo_name: str,
    file_path: str,
    owner: str,
    ref: str |None = Query(None),
):

    token = request.session.get("gh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authorized. Go to /auth/github first.")
    if not ref:
        ref = "main"

    # Получаем содержимое файла
    file_resp = await github.get(
        f"repos/{owner}/{repo_name}/contents/{file_path}",
        token=token,
        params={"ref": ref},
        headers=req_headers,
    )
    if file_resp.status_code == 404:
        raise HTTPException(status_code=404, detail="File not found or it's a directory")
    if file_resp.status_code >= 400:
        raise HTTPException(status_code=file_resp.status_code, detail=file_resp.text)

    data = file_resp.json()
    if isinstance(data, list):
        raise HTTPException(status_code=400, detail="Path refers to a directory, not a file")


    content_b64 = data.get("content") or ""
    decoded = base64.b64decode(content_b64, validate=False) if content_b64 else b""
    try:
        text = decoded.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File content is not text")

    return {
        "repo": repo_name,
        "ref": ref,
        "path": file_path,
        "content": text,
    }
