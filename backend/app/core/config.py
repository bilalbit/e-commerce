from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    salt: str

    ##phone number validator
    supported_regions:set
    default_region:str
    number_format:str

    model_config = SettingsConfigDict(env_file="../.env")

# use this for getting .env configs
@lru_cache
def get_settings():
    return Settings()

#use this for testing purpose only
setting_dep = Annotated[Settings, Depends(get_settings)]