import streamlit as st
from groq import Groq
import requests
import io
from PIL import Image

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="Heal-o", page_icon="🌙")
st.title("🌙 Heal-o")
st.caption("Hi Kimberley, aku Heal-O asisten pribadi kamu.")

# 2. Ambil Kunci Rahasia dari 'Brankas' Streamlit
GROQ_KEY = st.secrets["GROQ_API_KEY"]
HF_TOKEN = st.secrets["HF_TOKEN"]

client = Groq(api_key=GROQ_KEY)

# Fungsi buat bikin gambar (Hugging Face)
def generate_image(prompt):
    API_URL = "https://api-inference.huggingface.co"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    return response.content

# 3. Setting Identitas AI
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "Nama kamu Heal-o. Kamu teman curhat & brainstorming Gen Z yang hangat. Jika user minta gambar, jawablah dengan baik. Gunakan bahasa aku-kamu yang santai."}
    ]

# 4. Tampilkan Chat
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. Logika Interaksi
if prompt := st.chat_input("Mau cerita atau bikin ide apa hari ini?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # CEK: Apakah user minta gambar?
    if "gambar" in prompt.lower() or "lukis" in prompt.lower():
        with st.chat_message("assistant"):
            with st.spinner("Tunggu bentar ya, aku lukis dulu..."):
                try:
                    image_bytes = generate_image(prompt)
                    image = Image.open(io.BytesIO(image_bytes))
                    st.image(image, caption="Ini buat kamu ✨")
                    st.session_state.messages.append({"role": "assistant", "content": f"Aku sudah buatkan gambarnya: {prompt}"})
                except:
                    st.error("Waduh, pelukisnya lagi istirahat. Coba lagi nanti ya!")
    
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
