import streamlit as st

# タイトルと説明文の表示
st.title("ストリームリットの簡単なサンプルアプリ")
st.write("このサンプルでは、ストリームリットの使用方法を簡単に紹介します。")

# 数値入力の追加
num1 = st.number_input("最初の数値を入力してください:")
num2 = st.number_input("2番目の数値を入力してください:")
num3 = st.number_input("3番目の数値を入力してください:")

# ボタンの追加
submit_button = st.button("計算")

# 計算結果の表示
if submit_button:
    result = num1 * num2 * num3
    st.write(f"計算結果: {result}")
