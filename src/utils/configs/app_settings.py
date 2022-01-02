from pydantic import BaseSettings, Field
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()

class AppSettings(BaseSettings):
    PREFIX: str = Field(..., env='DKK_DISCORD_PREFIX')
    TOKEN: str = Field(..., env='DKK_DISCORD_TOKEN')
    DBMS: str = "postgres"
    DB_HOST: str
    DB_PORT: int = 5432
    DB_PASSWORD: str
    DB_USER: str
    DB_DATABASE: str
    COIN_NAME: str = "ข้างไข่คอยด์"

    class Config:
        env_prefix = 'DKK_'

@lru_cache()
def get_settings():
    return AppSettings()