# Pythonの公式イメージをベースに使用
FROM python:3.10

# 作業ディレクトリの設定
WORKDIR /usr/src/app

# 必要なパッケージのインストール
# discord.py とその依存関係をインストール
RUN pip install  "discord.py[voice]"
RUN pip install loguru pandas

RUN pip install -q -U google-generativeai
