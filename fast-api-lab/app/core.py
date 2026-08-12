from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Task Service"
    ENV: str = "development"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    MODEL_NAME: str = "openai/gpt-5.6-luna"

    # PostgreSQL Database 設定
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/task_db"

    # OpenRouter 設定
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
