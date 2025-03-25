from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.config import settings
from src.models.models import User, RefreshToken, PasswordResetToken
from src.schemas.auth import (
    UserCreate, UserLogin, UserResponse, Token, 
    PasswordReset, PasswordResetConfirm, TokenRefresh,
    MessageResponse
)
from src.utils.auth_utils import (
    get_password_hash, verify_password, create_token,
    verify_token, send_password_reset_email, generate_reset_token
)

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """新規ユーザー登録"""
    # メールアドレスの重複チェック
    stmt = select(User).where(User.email == user_data.email)
    if db.execute(stmt).scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # ユーザー作成
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """ユーザーログイン"""
    stmt = select(User).where(User.email == user_data.email)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user or not verify_password(user_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # アクセストークンとリフレッシュトークンを生成
    access_token = create_token(
        str(user.id),
        settings.ACCESS_TOKEN_EXPIRE_DELTA,
        "access"
    )
    refresh_token = create_token(
        str(user.id),
        settings.REFRESH_TOKEN_EXPIRE_DELTA,
        "refresh"
    )
    
    # リフレッシュトークンをデータベースに保存
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + settings.REFRESH_TOKEN_EXPIRE_DELTA
    )
    db.add(db_refresh_token)
    db.commit()
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    """リフレッシュトークンを使用して新しいアクセストークンを取得"""
    # リフレッシュトークンを検証
    token_payload = verify_token(token_data.refresh_token, "refresh")
    
    # データベースでリフレッシュトークンを確認
    stmt = select(RefreshToken).where(
        RefreshToken.token == token_data.refresh_token,
        RefreshToken.is_revoked == False
    )
    db_token = db.execute(stmt).scalar_one_or_none()
    
    if not db_token or db_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    # 古いリフレッシュトークンを無効化
    db_token.is_revoked = True
    
    # 新しいトークンを生成
    new_access_token = create_token(
        token_payload.sub,
        settings.ACCESS_TOKEN_EXPIRE_DELTA,
        "access"
    )
    new_refresh_token = create_token(
        token_payload.sub,
        settings.REFRESH_TOKEN_EXPIRE_DELTA,
        "refresh"
    )
    
    # 新しいリフレッシュトークンをデータベースに保存
    new_db_token = RefreshToken(
        user_id=db_token.user_id,
        token=new_refresh_token,
        expires_at=datetime.utcnow() + settings.REFRESH_TOKEN_EXPIRE_DELTA
    )
    db.add(new_db_token)
    db.commit()
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )

@router.post("/token/verify")
async def verify_token_endpoint(token: str, db: Session = Depends(get_db)):
    """トークンを検証してユーザー情報を返す"""
    token_data = verify_token(token)
    stmt = select(User).where(User.id == token_data.sub)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"user_id": str(user.id), "email": user.email}

@router.post("/password/reset", response_model=MessageResponse)
async def request_password_reset(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """パスワードリセットをリクエスト"""
    stmt = select(User).where(User.email == reset_data.email)
    user = db.execute(stmt).scalar_one_or_none()
    
    if not user:
        # ユーザーが存在しない場合でもセキュリティのため成功を装う
        return MessageResponse(message="If the email exists, a reset link has been sent")
    
    # 既存の未使用のリセットトークンを無効化
    stmt = (
        update(PasswordResetToken)
        .where(
            PasswordResetToken.user_id == user.id,
            PasswordResetToken.is_used == False
        )
        .values(is_used=True)
    )
    db.execute(stmt)
    
    # 新しいリセットトークンを生成
    token = generate_reset_token()
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=datetime.utcnow() + timedelta(hours=1)
    )
    db.add(reset_token)
    db.commit()
    
    # リセットメールを送信
    await send_password_reset_email(user.email, token)
    
    return MessageResponse(message="If the email exists, a reset link has been sent")

@router.post("/password/reset/confirm", response_model=MessageResponse)
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):
    """パスワードリセットを実行"""
    stmt = select(PasswordResetToken).where(
        PasswordResetToken.token == reset_data.token,
        PasswordResetToken.is_used == False,
        PasswordResetToken.expires_at > datetime.utcnow()
    )
    reset_token = db.execute(stmt).scalar_one_or_none()
    
    if not reset_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # パスワードを更新
    stmt = select(User).where(User.id == reset_token.user_id)
    user = db.execute(stmt).scalar_one_or_none()
    user.password_hash = get_password_hash(reset_data.new_password)
    
    # リセットトークンを使用済みにする
    reset_token.is_used = True
    
    # ユーザーの全てのリフレッシュトークンを無効化
    stmt = (
        update(RefreshToken)
        .where(
            RefreshToken.user_id == user.id,
            RefreshToken.is_revoked == False
        )
        .values(is_revoked=True)
    )
    db.execute(stmt)
    db.commit()
    
    return MessageResponse(message="Password has been reset successfully")
