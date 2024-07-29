from openai import OpenAI
import streamlit as st
import time

API_KEY = st.secrets['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

# streamlit의 자체 기능인 session_state에 thread관련 정보 저장 + 하나의 thread로 관리!!
if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id = st.session_state.thread_id
assistant_id = "asst_GyHpEq4rKyMTSm05AbShypNc" # 오토커넥트 1차

thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

st.header("오토커넥트 챗봇 1차")
st.write("**웹 서비스 UI는 언제든지 바뀔 수 있습니다!**")

for msg in thread_messages.data:
    with st.chat_message(msg.role):
        st.write(msg.content[0].text.value)

prompt = st.chat_input("오토커넥트 챗봇에게 물어보세요!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt,
    )
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id= assistant_id,
    )

    with st.spinner('오토커넥트 챗봇이 답변하는 중...'):
        while run.status != "completed":
            time.sleep(0.2)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    message = client.beta.threads.messages.list(
        thread_id=thread_id,
    )

    with st.chat_message(message.data[0].role):
        st.write(message.data[0].content[0].text.value)

    print(run)
    print(message)