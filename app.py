import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# ---- CONFIGURACIÓN DE PÁGINA ----
st.set_page_config(page_title="Conversión de Texto a Audio", page_icon="📖", layout="centered")

# ---- ESTILO VISUAL (TIPO LIBRO) ----
page_bg = """
<style>
body {
    background: linear-gradient(180deg, #f8f4e5 0%, #f1e8d9 100%);
    font-family: 'Georgia', serif;
    color: #3a2e2e;
}
h1, h2, h3, h4, h5 {
    color: #4b2e05;
    text-shadow: 1px 1px 2px rgba(150, 120, 50, 0.3);
}
.stButton>button {
    background: linear-gradient(90deg, #c49a6c, #b58c63);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    font-family: 'Georgia', serif;
    font-size: 1.1em;
    transition: all 0.3s ease-in-out;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #b58c63, #9c7a50);
    transform: scale(1.02);
}
.stTextArea textarea {
    background-color: #fcf8ef;
    border-radius: 10px;
    border: 1px solid #d1bfa7;
    color: #3a2e2e;
    font-family: 'Georgia', serif;
}
.sidebar .sidebar-content {
    background-color: #f4ead7;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---- CONTENIDO ----
st.title("📖 Conversión de Texto a Audio")

image = Image.open('gato_raton.png')
st.image(image, width=350)

with st.sidebar:
    st.subheader("✍️ Escribe o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una pequeña fábula")
st.write(
    '“¡Ay! —dijo el ratón—. El mundo se hace cada día más pequeño. '
    'Al principio era tan grande que le tenía miedo. Corría y corría y por cierto '
    'que me alegraba ver esos muros, a diestra y siniestra, en la distancia. '
    'Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto '
    'y ahí en el rincón está la trampa sobre la cual debo pasar. '
    '—Todo lo que debes hacer es cambiar de rumbo —dijo el gato… y se lo comió.”'
    '\n\n*Franz Kafka*'
)

st.markdown("### ¿Quieres escucharlo? Copia o escribe el texto abajo:")
text = st.text_area("🖋️ Ingrese el texto a escuchar:")

tld = 'com'
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
