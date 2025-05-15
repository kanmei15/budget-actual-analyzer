# Pythonの公式イメージをベースにする
FROM python:3.13-slim

# 作業ディレクトリを作成
WORKDIR /app

# 必要なファイルをコンテナにコピー
COPY requirements.txt /app/

# 必要なPythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースコードをコンテナにコピー
COPY . .

# Flaskアプリケーションを実行
CMD ["python", "/app/run.py"]