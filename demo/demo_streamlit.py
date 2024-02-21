import streamlit as st

# タイトルと説明文の表示
st.title("ストリームリットの簡単なサンプルアプリ")
st.write("このサンプルでは、ストリームリットの使用方法を簡単に紹介します。")

# テキスト入力の追加
name = st.text_input("あなたの名前を入力してください:")

# ボタンの追加
submit_button = st.button("送信")

# 送信ボタンがクリックされたときの処理
if submit_button:
    st.write(f"こんにちは、{name}さん！")
