# app/config.py
from functools import lru_cache
import os
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    # API configuration
    API_PREFIX : str
    API_VERSION : str
    TEST_MODE : bool

    # Database configuration
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    APP_DATABASE : str
    POSTGRES_HOST : str
    HOST : str
    POSTGRES_PORT : str
    DATABASE_URL : str

    # JWT configuration
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    REFRESH_TOKEN_EXPIRE_DAYS : int
    DEFAULT_EXPIRE_MINUTES : int
    

    class Config:
        # Use the ENV_FILE environment variable or default to .env
        env_file = os.getenv("ENV_FILE", ".env")


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()