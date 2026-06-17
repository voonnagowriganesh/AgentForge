from functools import lru_cache
import os

from dotenv import load_dotenv

from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    APP_NAME: str = "AI Agent Platform"

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

    MODEL_NAME: str = "llama-3.3-70b-versatile"

    RAG_THRESHOLD: float = 0.5

    LOG_LEVEL: str = "INFO"

    class Config:

        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()
