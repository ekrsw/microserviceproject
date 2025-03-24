from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Any


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="your-secret-key", json_schema_extra={"env": "SECRET_KEY"})

    # トークン設定
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS設定
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",  # フロントエンドアプリURL
        "http://localhost:8000",  # 開発用
    ]

    # サービスのURL
    AUTH_SERVICE_URL: str = Field(default="http://localhost:8001", json_schema_extra={"env": "AUTH_SERVICE_URL"})
    TODO_SERVICE_URL: str = Field(default="http://localhost:8002", json_schema_extra={"env": "TODO_SERVICE_URL"})

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="",
    )

settings = Settings()