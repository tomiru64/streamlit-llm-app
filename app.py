from dotenv import load_dotenv
import os, streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# --- キー取得 ---
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
if not api_key:
    st.error("OPENAI_API_KEY がありません"); st.stop()
# ----------------------------------------------------

st.title("LLM機能を搭載したWebアプリ")

st.markdown("""
### 💡 アプリの概要

このアプリは、あなたの入力内容に対して、AIが専門家として回答を行うチャットアプリです。  
専門家の分野はラジオボタンで選択でき、選んだ分野に応じて、AIがその分野の知識に基づいたアドバイスや説明を行います。
""")

st.markdown("""
### 🛠 操作方法

1. **専門家の種類を選ぶ**  
　画面上のラジオボタンから、相談したい分野の専門家を選択してください。

2. **質問を入力する**  
　テキストボックスに聞きたいことや相談内容を入力してください。

3. **送信する**  
　送信ボタンを押すと、選んだ専門家としてAIが回答します。
""")

st.markdown("""
### 📌 注意事項

- AIはあくまで参考として情報を提供するものであり、実際の医療・法律・財務などの判断は専門機関への相談を推奨します。
- 入力内容はAI処理のために一時的に送信されます。個人情報などの入力にはご注意ください。
""")

st.divider()

selected_item = st.radio(
    "質問したい専門家を選択してください。",
    ["AIに関する専門家", "健康に関する専門家"]
)

input_message = st.text_input(label="質問を入力してください")

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)

def get_llm_response(input_text, selected_expert):
    """
    この関数は、入力テキストと選択された専門家の種類を引数として受け取り、
    LLMからの応答を返します。
    """

    # 選択された専門家に基づいてシステムメッセージを定義
    system_message_content = f"You are an expert in {selected_expert}. Provide helpful and accurate responses."

    messages = [
        SystemMessage(content=system_message_content),
        HumanMessage(content=input_text),
    ]

    # LLMからの応答を取得
    response = llm(messages)
    return response.content

if st.button("実行") and input_message:
    st.divider()
    response = get_llm_response(input_message, selected_item)
    st.write(response)