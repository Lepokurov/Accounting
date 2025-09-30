from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    api_token: str = Field(alias="API_TOKEN")
    database_url: str = Field(alias="DATABASE_URL")
    sync_database_url: str = Field(alias="SYNC_DATABASE_URL")  # for Alembic
    app_env: str = Field(default="dev", alias="APP_ENV")

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
