from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import auth
from src.core.database import engine, Base

# データベーステーブルの作成
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="認証サービス",
    description="ユーザー認証とアカウント管理を提供するマイクロサービス",
    version="1.0.0"
)

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切なオリジンを指定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルーターの登録
app.include_router(
    auth.router,
    prefix="/api/v1",
    tags=["認証"]
)

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}
