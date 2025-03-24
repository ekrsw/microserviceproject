from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from src.core.config import settings
from src.schemas.auth import TokenPayload
import uuid

# パスワードハッシュ化設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# メール設定
mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

fastmail = FastMail(mail_config)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証する"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化する"""
    return pwd_context.hash(password)

def create_token(user_id: str, expires_delta: timedelta, token_type: str = "access") -> str:
    """JWTトークンを生成する"""
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": token_type
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> TokenPayload:
    """トークンを検証する"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)
        
        if token_data.type != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}",
            )
            
        return token_data
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

async def send_password_reset_email(email: str, token: str):
    """パスワードリセットメールを送信する"""
    # TODO: 実際のフロントエンドURLに置き換える
    reset_url = f"http://localhost:3000/reset-password?token={token}"
    
    message = MessageSchema(
        subject="パスワードリセット",
        recipients=[email],
        body=f"""
        パスワードリセットのリクエストを受け付けました。
        
        以下のリンクをクリックしてパスワードをリセットしてください：
        {reset_url}
        
        このリンクは1時間後に無効になります。
        
        このメールに心当たりがない場合は、無視してください。
        """,
    )
    
    await fastmail.send_message(message)

def generate_reset_token() -> str:
    """パスワードリセット用のトークンを生成する"""
    return str(uuid.uuid4())
