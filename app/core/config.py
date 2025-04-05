from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str  # Use SQLite initially
    secret_key: str  # Generate a secure key
    algorithm: str
    access_token_expire_minutes: int
    salt: str

    model_config = SettingsConfigDict(env_file="../.env")


@lru_cache
def get_settings():
    return Settings()

setting_dep = Annotated[Settings, Depends(get_settings)]