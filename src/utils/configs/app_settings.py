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
    COIN_NAME: str = "ข้างไข่คอยน์"
    MAX_BET: float = 20.0
    MIN_BET: float = 0.1
    SELF_MESSAGE_DELETE_TIME: int
    PRICE: float = 0.001

    class Config:
        env_prefix = 'DKK_'

@lru_cache()
def get_settings():
    return AppSettings()