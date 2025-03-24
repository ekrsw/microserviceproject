from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime
from uuid import UUID

# リクエストスキーマ
class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)  # 最小8文字のパスワード

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=8)

class TokenRefresh(BaseModel):
    refresh_token: str

# レスポンススキーマ
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str  # user_id
    exp: datetime
    type: str  # "access" or "refresh"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    message: str
