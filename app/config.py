from pydantic_settings import BaseSettings, SettingsConfigDict
from authlib.integrations.starlette_client import OAuth
from pydantic import Field


class Settings(BaseSettings):
    GITHUB_CLIENT_ID: str = Field("", validation_alias="GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET:str = Field("", validation_alias="GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI: str = Field("", validation_alias="GITHUB_REDIRECT_URI")
    GITHUB_CLIENT_KWARGS: dict = {'scope': 'repo'}

    ACCESS_TOKEN_URL: str = "https://github.com/login/oauth/access_token"
    AUTHORIZE_URL: str = "https://github.com/login/oauth/authorize"
    API_BASE_URL: str = "https://api.github.com/"

    SECRET_KEY: str = Field("", validation_alias="SECRET_KEY")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

oauth = OAuth()
oauth.register(
    name="github",
    client_id=settings.GITHUB_CLIENT_ID,
    client_secret=settings.GITHUB_CLIENT_SECRET,
    access_token_url=settings.ACCESS_TOKEN_URL,
    authorize_url=settings.AUTHORIZE_URL,
    api_base_url=settings.API_BASE_URL
)
github = oauth.create_client('github')
