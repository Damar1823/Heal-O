import streamlit as st
from groq import Groq

st.set_page_config(page_title="Heal-o", page_icon="🌙")
st.title("🌙 Heal-o")
st.write("Halo, Heal-o disini siap untuk membantu.")

try:
    client = Groq(api_key="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")
except:
    st.error("API Key belum bener nih. Cek lagi ya!")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Nama kamu Heal-o. Kamu teman curhat Gen Z yang santai, empati, dan gak menghakimi. Pakai bahasa aku-kamu yang hangat. Jangan kaku kayak robot."}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Lagi ngerasa apa hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages
        )
        msg = response.choices[0].message.content
        st.markdown(msg)
    st.session_state.messages.append({"role": "assistant", "content": msg})
