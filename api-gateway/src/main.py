from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import auth
from src.middlewares.auth_middleware import verify_token
from src.core.config import settings

app = FastAPI(title="API Gateway")

# CORSミドルウェア設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# サービスのルート設定
app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(todos.router, prefix="/todos", tags=["todos"], dependencies=[Depends(verify_token)])

@app.get("/health")
def health_check():
    return {"status": "ok"}