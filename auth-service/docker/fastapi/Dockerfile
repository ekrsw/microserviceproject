FROM python:3.12.9-slim

# 作業ディレクトリの設定
WORKDIR /workdir

# 必要な環境変数を設定
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# PostgreSQLクライアントライブラリをインストール
RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev gcc python3-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 依存関係のインストール
COPY ./requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ソースコードのコピー
COPY . /workdir

# 非rootユーザーを作成して実行（セキュリティ向上）
RUN adduser --disabled-password --gecos "" appuser && \
    # ボリュームマウントポイントの所有権を変更
    mkdir -p /workdir/.pytest_cache && \
    chown -R appuser:appuser /workdir

# Uvicorn でアプリケーションを起動（ワーカー数を制限）
# 環境変数からホストとポートを取得するためにエントリーポイントスクリプトを使用
COPY ./docker/fastapi/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]