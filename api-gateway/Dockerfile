FROM python:3.9-slim

WORKDIR /app

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY . .

# アプリケーションを実行
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]