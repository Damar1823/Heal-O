import streamlit as st
from groq import Groq
import requests
import io

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Heal-o", page_icon="🌙")
st.title("🌙 Heal-o")
st.caption("Teman curhat & kreatifmu. Ketik 'Gambar [sesuatu]' kalau mau aku melukis.")

# 2. Ambil Kunci Rahasia dari 'Brankas' Streamlit
# Pastikan kamu sudah isi GROQ_API_KEY dan HF_TOKEN di menu Secrets Streamlit!
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    HF_TOKEN = st.secrets["HF_TOKEN"]
    client = Groq(api_key=GROQ_KEY)
except:
    st.error("Waduh, kunci brankas (Secrets) belum lengkap nih!")

# Fungsi buat panggil pelukis (Hugging Face)
def generate_image(prompt_text):
    API_URL = "https://api-inference.huggingface.co"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt_text})
    return response.content

# 3. Setting Memori Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Nama kamu Heal-o. Kamu teman curhat & brainstorming Gen Z yang hangat. Gunakan bahasa aku-kamu yang santai. Kamu punya fitur melukis jika diminta."}
    ]

# Tampilkan Chat Lama
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. Logika Utama
if prompt := st.chat_input("Mau cerita atau bikin ide apa hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # CEK: Apakah user minta gambar?
    kata_kunci =
    if any(kata in prompt.lower() for kata in kata_kunci):
        with st.chat_message("assistant"):
            with st.spinner("Tunggu bentar ya, aku lukis dulu..."):
                try:
                    image_bytes = generate_image(prompt)
                    st.image(image_bytes, caption="Ini buat kamu ✨")
                    st.session_state.messages.append({"role": "assistant", "content": f"Aku sudah buatkan gambarnya untukmu!"})
                except:
                    st.error("Yah, pelukisnya lagi capek. Coba lagi nanti ya!")
    
    # JIKA: Curhat/Brainstorming biasa
    else:
        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages
            )
            msg = response.choices[0].message.content
            st.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})
