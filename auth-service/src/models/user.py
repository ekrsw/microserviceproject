from typing import Any, Dict, Optional, List, Type, TypeVar, Union
from passlib.context import CryptContext

from pydantic import BaseModel
from typing import Optional
from sqlalchemy import String, Select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import ModelBaseMixin, T
from src.core.session import AsyncContextManager
from src.schemas.user_schema import UserCreate, UserPasswordSchema, UserUpdate


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class User(ModelBaseMixin):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

    async def verify_password(self, plain_password: str) -> bool:
        """入力されたパスワードがハッシュと一致するかを確かめる。

        Args:
            plain_password (str): 検証する平文パスワード

        Returns:
            bool: パスワードが一致する場合はTrue、それ以外はFalse
        """
        return pwd_context.verify(plain_password, self.hashed_password)
    
    @staticmethod
    async def set_password(plain_password: str) -> str:
        """パスワードをハッシュ化して返す。

        Args:
            plain_password (str): ハッシュ化する平文パスワード

        Returns:
            str: ハッシュ化されたパスワード
        """
        cleaned_password = UserPasswordSchema(password=plain_password).password
        return pwd_context.hash(cleaned_password)
    
    @classmethod
    async def create_user(
        cls: Type[T],
        *,
        username: str,
        password: str,
        ) -> T:
        """ユーザー作成メソッド。

        AsyncContextManagerのコンテキスト終了時に暗黙的にcommitされます。

        Args:
            obj_in (Dict[str, Any]): ユーザー作成に必要な情報を含む辞書。"password"キーが含まれる場合は自動的にハッシュ化されます。

        Returns:
            T: 作成されたユーザーオブジェクト（データベースにはまだcommitされていない状態）
        """
        async with AsyncContextManager() as session:
            user_create = UserCreate(username=username, password=password)
            validated_password = user_create.password
            validated_username = user_create.username
            hashed_password = await cls.set_password(validated_password)
            new_user = cls(username=validated_username, hashed_password=hashed_password)
            session.add(new_user)
        return new_user


    @classmethod
    async def get_all_users(cls: Type[T], include_deleted: bool = False) -> List[T]:
        """全てのユーザーを取得する。

        Args:
            include_deleted (bool, optional): 論理削除済みのユーザーも含めるかどうか。デフォルトはFalse。

        Returns:
            List[T]: ユーザーオブジェクトのリスト
        """
        async with AsyncContextManager() as session:
            stmt = Select(cls)
            if include_deleted:
                stmt = stmt.execution_options(include_deleted=True)
            result = await session.execute(stmt)
            users = result.scalars().all()
        return users

    @classmethod
    async def get_user_by_id(cls: Type[T], user_id: str, include_deleted: bool = False) -> T:
        """ユーザーIDからユーザーを取得する。

        Args:
            user_id (str): ユーザーID
            include_deleted (bool, optional): 論理削除済みのユーザーも含めて取得するかどうか。デフォルトはFalse。

        Returns:
            T: 取得したユーザーオブジェクト。存在しない場合はNone。
        """
        async with AsyncContextManager() as session:
            stmt = Select(cls).where(cls.id == user_id)
            if include_deleted:
                stmt = stmt.execution_options(include_deleted=True)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
        return user
    
    @classmethod
    async def get_user_by_username(cls: Type[T], username: str, include_deleted: bool = False) -> Optional[T]:
        """ユーザー名からユーザーを取得する。

        Args:
            username (str): ユーザー名
            include_deleted (bool, optional): 論理削除済みのユーザーも含めて取得するかどうか。デフォルトはFalse。

        Returns:
            Optional[T]: 取得したユーザーオブジェクト。存在しない場合はNone。
        """
        async with AsyncContextManager() as session:
            stmt = Select(cls).where(cls.username == username)
            if include_deleted:
                stmt = stmt.execution_options(include_deleted=True)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
        return user
    
    @classmethod
    async def update_user(cls: Type[T],
                          id: str,
                          username: Optional[str] = None,
                          password: Optional[str] = None
                          ) -> T:
        """汎用ユーザー情報を更新する。

        Args:
            db_obj (T): 更新対象のユーザーオブジェクト
            obj_in (Dict[str, Any]): 更新情報

        Returns:
            T: 更新後のユーザーオブジェクト

        Raises:
            ValueError: 更新対象のユーザーオブジェクトが存在しない場合
            Exception: 論理削除済みのユーザーを更新しようとした場合
        """
        update_data = UserUpdate(username=username, password=password)
        validated_username = update_data.username
        validated_password = update_data.password
        async with AsyncContextManager() as session:
            # 最新のユーザー情報を取得して削除状態を確認
            current_user = await cls.get_user_by_id(id)
            if current_user is None:
                raise ValueError("User not found")

            # ユーザー情報を更新
            if validated_username:
                current_user.username = validated_username

            # パスワードを特別に処理
            if validated_password:
                current_user.hashed_password = await cls.set_password(validated_password)
            
            session.add(current_user)
            await session.commit()
            await session.refresh(current_user)
        return current_user
    
    @classmethod
    async def delete_user(cls: Type[T], user_id: str):
        """ユーザーを論理削除する。

        Args:
            user_id (str): 削除するユーザーのID
        """
        async with AsyncContextManager() as session:
            user = await cls.get_user_by_id(user_id, include_deleted=True)
            user.deleted_at = func.now()
            session.add(user)
    
    @classmethod
    async def delete_user_permanently(cls: Type[T], user_id: str) -> None:
        """ユーザーを物理削除する。

        Args:
            user_id (str): 削除するユーザーのID

        Raises:
            ValueError: 指定されたIDのユーザーが存在しない場合
        """
        async with AsyncContextManager() as session:
            user = await cls.get_user_by_id(user_id, include_deleted=True)
            await session.delete(user)
