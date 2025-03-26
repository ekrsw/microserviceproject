import datetime

from typing import Any, Dict, Optional, List, Type, TypeVar, Union
from passlib.context import CryptContext

from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Boolean, DateTime, String, Select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import ModelBaseMixin, T
from .token import RefreshToken, PasswordResetToken
from src.core.session import AsyncContextManager
from src.schemas.user_schema import UserCreate, UserPasswordSchema, UserUpdate


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class User(ModelBaseMixin):
    __tablename__ = "users"
    
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    refresh_tokens: Mapped[List[RefreshToken]] = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    password_reset_tokens: Mapped[List[PasswordResetToken]] = relationship("PasswordResetToken", back_populates="user", cascade="all, delete-orphan")