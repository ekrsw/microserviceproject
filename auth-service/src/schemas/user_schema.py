from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional
from uuid import UUID


class UserBase(BaseModel):
    username: Optional[str] = None
    # ここにフィールドを追加

    @field_validator("username")
    def username_valid(cls, username):
        if username is None:
            return username
        if not isinstance(username, str):
            raise ValueError("username must be a string")
        username = username.strip()
        if not username:
            raise ValueError("username must not be empty")
        if len(username) < 3 or len(username) > 100:
            raise ValueError("username must be between 3 and 100 characters")
        return username

class UserResponseBase(BaseModel):
    id: UUID
    username: str
    model_config = ConfigDict(from_attributes=True)
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PasswordMixin(BaseModel):
    password: str

    @field_validator("password")
    def password_valid(cls, password):
        if password is not None:
            if not password.strip():
                raise ValueError("password must not be empty")
            if len(password) < 8 or len(password) > 30:
                raise ValueError("password must be between 8 and 30 characters")
        return password

class UserResponse(UserResponseBase):
    pass


class UserCreate(UserBase, PasswordMixin):
    username: str


class UserUpdate(UserBase):
    password: Optional[str] = None

    @field_validator("password")
    def password_valid(cls, password):
        if password is not None:
            if not password.strip():
                raise ValueError("password must not be empty")
            if len(password) < 8 or len(password) > 30:
                raise ValueError("password must be between 8 and 30 characters")
        return password


class UserPasswordSchema(PasswordMixin):
    """パスワードのバリデーション用スキーマ"""
    pass