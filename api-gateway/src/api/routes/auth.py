from fastapi import APIRouter, Request, Response, HTTPException, status
import httpx
import src.core.config as settings

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    body = await request.json()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTH_SERVICE_URL}/api/v1/users/register",
                json=body
            )

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Authentication service error: {str(exc)}"
            )

@router.post("/login")
async def login(request: Request):
    body = await request.json()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.AUTH_SERVICE_URL}/api/v1/auth/login",
                json=body
            )

            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Authentication service error: {str(exc)}"
            )