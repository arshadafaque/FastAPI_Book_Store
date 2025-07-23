from pydantic_settings import BaseSettings
from pathlib import Path

class Setting(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_HOST:str
    REDIS_PORT:int

    model_config = {
        "env_file": str(Path(__file__).resolve().parent / ".env"),
        "extra": "ignore"
    }

config = Setting()
