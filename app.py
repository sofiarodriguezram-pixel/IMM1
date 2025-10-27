import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ---- CONFIGURACIÓN DE PÁGINA ----
st.set_page_config(page_title="Conversión de Texto a Audio", page_icon="📜", layout="centered")

# ---- ESTILO LIBRO ANTIGUO CON FONDO CAFÉ CLARO ----
book_style = """
<style>
.stApp {
    background: radial-gradient(circle at center, #f4e6c1 0%, #e7d3a1 40%, #d8b97a 90%);
    font-family: 'Garamond', 'Georgia', serif;
    color: #3a2a16;
    padding: 2em;
}

h1, h2, h3, h4, h5 {
    color: #4b2e05;
    text-shadow: 2px 2px 4px rgba(60, 40, 15, 0.4);
    font-family: 'Garamond', serif;
    letter-spacing: 1px;
}

.stButton>button {
    background: linear-gradient(90deg, #a67c52, #8b5a2b);
    color: #fff8e7;
    border: 1px solid #5c3a1a;
    border-radius: 12px;
    padding: 0.6em 1.4em;
    font-family: 'Garamond', serif;
    font-size: 1.1em;
    box-shadow: 2px 2px 5px rgba(80, 50, 20, 0.4);
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #8b5a2b, #6b4221);
    transform: scale(1.03);
}

.stTextArea textarea {
    background-color: #f9f5e8;
    border-radius: 10px;
    border: 1px solid #c1a77a;
    color: #3b2a1a;
    font-family: 'Garamond', serif;
    font-size: 1.05em;
    line-height: 1.5em;
}

.sidebar .sidebar-content {
    background-color: #e9d7b5;
    color: #3b2a1a;
    border-right: 2px solid #c9b07d;
    font-family: 'Garamond', serif;
}

a {
    color: #6b4221 !important;
    text-decoration: none !important;
    font-weight: bold;
}
a:hover {
    color: #4b2e05 !important;
    text-shadow: 1px 1px 2px rgba(70, 40, 10, 0.3);
}
</style>
"""
st.markdown(book_style, unsafe_allow_html=True)

# ---- CONTENIDO ----
st.title("📜 Conversión de Texto a Audio")

image = Image.open('gato_raton.png')
st.image(image, width=350, caption="Fábula del gato y el ratón — Kafka")

with st.sidebar:
    st.subheader("✍️ Escribe o selecciona texto para escuchar.")
    st.markdown("---")

try:
    os.mkdir("temp")
except:
    pass

st.markdown("## Una pequeña fábula")
st.write(
    '“¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño. '
    'Al principio era tan grande que le tenía miedo. Corría y corría y por cierto '
    'que me alegraba ver esos muros, a diestra y siniestra, en la distancia. '
    'Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto '
    'y ahí en el rincón está la trampa sobre la cual debo pasar. '
    '—Todo lo que debes hacer es cambiar de rumbo —dijo el gato… y se lo comió.”'
    '\n\n*Franz Kafka*'
)

st.markdown("### 📖 ¿Quieres escucharlo? Copia o escribe el texto abajo:")
text = st.text_area("🖋️ Ingrese el texto a escuchar:")

option_lang = st.selectbox("🌍 Selecciona el idioma", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, text

if st.button("🎧 Convertir a Audio"):
    result, output_text = text_to_speech(text, 'com', lg)
    audio_file = open(f"temp/{result}.mp3", "rb")
    audio_bytes = audio_file.read()
    st.markdown("### 🎵 Tu audio:")
    st.audio(audio_bytes, format="audio/mp3", start_time=0)

    with open(f"temp/{result}.mp3", "rb") as f:
        data = f.read()

    def get_binary_file_downloader_html(bin_file, file_label='File'):
        bin_str = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">📥 Descargar {file_label}</a>'
        return href

    st.markdown(get_binary_file_downloader_html("audio.mp3", file_label="Audio"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
