from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from src.core.config import settings

security = HTTPBearer()

async def verify_token(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    token = credentials.credentials

    # 認証サービス二トークン検証リクエストを送信
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTH_SERCICE_URL}/api/v1/token/verify",
                json={"token": token}
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # 認証されたユーザー情報
            user_data = response.json()

            # リクエストオブジェクトにユーザー情報を保存
            request.state.user = user_data

            return user_data
        
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable",
            )