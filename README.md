todo-app/
│
├── api-gateway/ # API ゲートウェイサービス
│ ├── app/
│ │ ├── api/ # API 定義
│ │ │ ├── **init**.py
│ │ │ ├── routes/ # ルーティング
│ │ │ │ ├── **init**.py
│ │ │ │ ├── auth.py # 認証サービスへのルーティング
│ │ │ │ └── todos.py # TODO サービスへのルーティング
│ │ ├── core/ # コア設定
│ │ │ ├── **init**.py
│ │ │ ├── config.py # 環境設定
│ │ │ └── security.py # セキュリティ関連
│ │ ├── middlewares/ # ミドルウェア
│ │ │ ├── **init**.py
│ │ │ └── auth_middleware.py # 認証ミドルウェア
│ │ └── main.py # アプリケーションエントリポイント
│ ├── tests/ # テスト
│ ├── Dockerfile
│ ├── pyproject.toml # 依存関係管理 (Poetry)
│ ├── requirements.txt # 依存関係リスト
│ └── README.md
│
├── auth-service/ # 認証サービス
│ ├── app/
│ │ ├── api/ # API 定義
│ │ │ ├── **init**.py
│ │ │ ├── endpoints/ # エンドポイント
│ │ │ │ ├── **init**.py
│ │ │ │ ├── login.py # ログイン API
│ │ │ │ ├── users.py # ユーザー管理 API
│ │ │ │ └── token.py # トークン検証 API
│ │ ├── core/ # コア設定
│ │ │ ├── **init**.py
│ │ │ ├── config.py # 環境設定
│ │ │ └── security.py # JWT 認証等
│ │ ├── db/ # データベース関連
│ │ │ ├── **init**.py
│ │ │ ├── base.py # DB 基本設定
│ │ │ └── session.py # DB セッション
│ │ ├── models/ # SQLAlchemy モデル
│ │ │ ├── **init**.py
│ │ │ └── user.py # ユーザーモデル
│ │ ├── schemas/ # Pydantic スキーマ
│ │ │ ├── **init**.py
│ │ │ ├── token.py # トークンスキーマ
│ │ │ └── user.py # ユーザースキーマ
│ │ ├── crud/ # CRUD 操作
│ │ │ ├── **init**.py
│ │ │ └── user.py # ユーザー CRUD
│ │ └── main.py # アプリケーションエントリポイント
│ ├── alembic/ # マイグレーション
│ │ ├── versions/ # マイグレーションバージョン
│ │ └── alembic.ini # Alembic 設定
│ ├── tests/ # テスト
│ ├── Dockerfile
│ ├── pyproject.toml # 依存関係管理 (Poetry)
│ ├── requirements.txt # 依存関係リスト
│ └── README.md
│
├── todo-service/ # TODO サービス
│ ├── app/
│ │ ├── api/ # API 定義
│ │ │ ├── **init**.py
│ │ │ ├── endpoints/ # エンドポイント
│ │ │ │ ├── **init**.py
│ │ │ │ └── todos.py # TODO の CRUD API
│ │ ├── core/ # コア設定
│ │ │ ├── **init**.py
│ │ │ ├── config.py # 環境設定
│ │ │ └── security.py # トークン検証等
│ │ ├── db/ # データベース関連
│ │ │ ├── **init**.py
│ │ │ ├── base.py # DB 基本設定
│ │ │ └── session.py # DB セッション
│ │ ├── models/ # SQLAlchemy モデル
│ │ │ ├── **init**.py
│ │ │ └── todo.py # TODO モデル
│ │ ├── schemas/ # Pydantic スキーマ
│ │ │ ├── **init**.py
│ │ │ └── todo.py # TODO スキーマ
│ │ ├── crud/ # CRUD 操作
│ │ │ ├── **init**.py
│ │ │ └── todo.py # TODO CRUD
│ │ └── main.py # アプリケーションエントリポイント
│ ├── alembic/ # マイグレーション
│ │ ├── versions/ # マイグレーションバージョン
│ │ └── alembic.ini # Alembic 設定
│ ├── tests/ # テスト
│ ├── Dockerfile
│ ├── pyproject.toml # 依存関係管理 (Poetry)
│ ├── requirements.txt # 依存関係リスト
│ └── README.md
│
├── docker-compose.yml # ローカル開発環境構成
├── .env.example # 環境変数サンプル
├── .gitignore # Git の除外設定
├── kubernetes/ # Kubernetes 構成ファイル
│ ├── api-gateway/
│ ├── auth-service/
│ └── todo-service/
│
└── README.md # プロジェクト全体の説明
