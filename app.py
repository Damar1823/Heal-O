import streamlit as st
from groq import Groq
import requests

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Heal-o", page_icon="🌙")
st.title("🌙 Heal-o")
st.caption("Teman curhat & kreatifmu. Bilang 'Gambar [sesuatu]' kalau mau aku melukis.")

# 2. Ambil Kunci Rahasia
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    HF_TOKEN = st.secrets["HF_TOKEN"]
    client = Groq(api_key=GROQ_KEY)
except:
    st.error("Cek menu Secrets di Streamlit! Masukkan GROQ_API_KEY dan HF_TOKEN dulu.")

# Fungsi panggil pelukis (Hugging Face)
def generate_image(prompt_text):
    API_URL = "https://api-inference.huggingface.co"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt_text})
    if response.status_code != 200:
        raise Exception("Gagal panggil pelukis")
    return response.content

# 3. Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "Nama kamu Heal-o. Kamu teman curhat Gen Z yang hangat. Kamu bisa melukis jika diminta."}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Logika Chat & Gambar
if prompt := st.chat_input("Mau cerita atau bikin ide apa hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    input_user = prompt.lower()
    
    # LOGIKA BARU: Cek kata kunci satu-satu biar nggak error syntax
    minta_gambar = False
    if "gambar" in input_user or "lukis" in input_user or "foto" in input_user or "image" in input_user:
        minta_gambar = True
    
    if minta_gambar:
        with st.chat_message("assistant"):
            with st.spinner("Tunggu bentar ya, aku lukis dulu... ✨"):
                try:
                    image_bytes = generate_image(prompt)
                    st.image(image_bytes, caption="Ini buat kamu 🌙")
                    st.session_state.messages.append({"role": "assistant", "content": "Aku sudah buatkan gambarnya!"})
                except:
                    st.error("Waduh, pelukisnya lagi antri. Coba klik kirim lagi ya!")
    else:
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=st.session_state.messages)
                msg = response.choices[0].message.content
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})
            except:
                st.error("Aduh, aku lagi loading lama. Coba kirim pesannya lagi ya!")
