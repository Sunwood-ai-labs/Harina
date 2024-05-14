# Pythonの公式イメージをベースに使用
FROM python:3.10

# 作業ディレクトリの設定
WORKDIR /app

RUN apt update -y
RUN apt upgrade -y

# 必要なパッケージのインストール
# discord.py とその依存関係をインストール

RUN pip install --upgrade pip
RUN pip install  "discord.py[voice]"
RUN pip install loguru pandas termcolor art litellm

# RUN pip install -q -U google-generativeai
RUN pip install anthropic
