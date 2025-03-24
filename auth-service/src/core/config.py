from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict, EmailStr
from typing import Optional
from datetime import timedelta

class Settings(BaseSettings):
    # データベース設定
    DATABASE_URL: str = Field(..., json_schema_extra={"env": "DATABASE_URL"})

    # JWT設定
    SECRET_KEY: str = Field(..., json_schema_extra={"env": "SECRET_KEY"})
    ALGORITHM: str = Field(default="HS256", json_schema_extra={"env": "ALGORITHM"})
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, json_schema_extra={"env": "ACCESS_TOKEN_EXPIRE_MINUTES"})
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, json_schema_extra={"env": "REFRESH_TOKEN_EXPIRE_DAYS"})

    # メール設定
    MAIL_USERNAME: str = Field(..., json_schema_extra={"env": "MAIL_USERNAME"})
    MAIL_PASSWORD: str = Field(..., json_schema_extra={"env": "MAIL_PASSWORD"})
    MAIL_FROM: EmailStr = Field(..., json_schema_extra={"env": "MAIL_FROM"})
    MAIL_PORT: int = Field(..., json_schema_extra={"env": "MAIL_PORT"})
    MAIL_SERVER: str = Field(..., json_schema_extra={"env": "MAIL_SERVER"})
    MAIL_STARTTLS: bool = Field(default=False, json_schema_extra={"env": "MAIL_STARTTLS"})
    MAIL_SSL_TLS: bool = Field(default=True, json_schema_extra={"env": "MAIL_SSL_TLS"})

    # レート制限設定
    LOGIN_RATE_LIMIT: str = Field(default="5/minute", json_schema_extra={"env": "LOGIN_RATE_LIMIT"})
    PASSWORD_RESET_RATE_LIMIT: str = Field(default="3/hour", json_schema_extra={"env": "PASSWORD_RESET_RATE_LIMIT"})

    @property
    def ACCESS_TOKEN_EXPIRE_DELTA(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)

    @property
    def REFRESH_TOKEN_EXPIRE_DELTA(self) -> timedelta:
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
        env_prefix="",
    )

settings = Settings()
