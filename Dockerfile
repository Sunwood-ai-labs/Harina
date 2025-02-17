# Pythonの公式イメージをベースに使用
FROM python:3.10

# 作業ディレクトリの設定
WORKDIR /app

RUN apt update -y
RUN apt upgrade -y

# 必要なパッケージのインストール
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install anthropic
