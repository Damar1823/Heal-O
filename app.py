import streamlit as st
from groq import Groq
import requests

# 1. Tampilan Aplikasi
st.set_page_config(page_title="Heal-o", page_icon="🌙")
st.title("🌙 Heal-o")
st.caption("Teman curhat & kreatifmu. Bilang 'Gambar [sesuatu]' kalau mau aku melukis.")

# 2. Koneksi ke Brankas (Secrets)
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    HF_TOKEN = st.secrets["HF_TOKEN"]
    client = Groq(api_key=GROQ_KEY)
except:
    st.error("Cek menu Secrets di Streamlit ya, kuncinya belum lengkap!")

# Fungsi buat panggil pelukis (Hugging Face)
def generate_image(prompt_text):
    API_URL = "https://api-inference.huggingface.co"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt_text})
    return response.content

# 3. Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Nama kamu Heal-o. Kamu teman curhat Gen Z yang hangat. Kamu bisa melukis jika diminta."}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Logika Chat & Gambar
if prompt := st.chat_input("Lagi ngerasa apa hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # BARIS INI YANG TADI KOSONG (SUDAH DIPERBAIKI):
    if any(kata in prompt.lower() for kata in):
        with st.chat_message("assistant"):
            with st.spinner("Tunggu bentar ya, aku lukis dulu..."):
                try:
                    image_bytes = generate_image(prompt)
                    st.image(image_bytes, caption="Ini buat kamu ✨")
                    st.session_state.messages.append({"role": "assistant", "content": "Aku sudah buatkan gambarnya!"})
                except:
                    st.error("Pelukisnya lagi capek. Coba lagi nanti!")
    else:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=st.session_state.messages)
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
