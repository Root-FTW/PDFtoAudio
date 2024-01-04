import streamlit as st
from openai import GPT3Client
import fitz  # PyMuPDF
from pydub import AudioSegment
from io import BytesIO

# Inicializar el cliente de OpenAI con un valor temporal para la clave API
openai_client = GPT3Client(api_key="temp")

# Función para convertir texto a audio utilizando OpenAI
def text_to_speech(text, api_key):
    # Configurar el cliente de OpenAI con la clave API proporcionada
    openai_client.api_key = api_key
    
    # Supongamos que la API de OpenAI tiene un método para convertir texto a voz
    # Esta es una suposición y necesitarás reemplazarla con el código real de la API
    audio_data = openai_client.text_to_speech(text)
    return audio_data

# Título de la aplicación
st.title('Conversor de PDF a Audiolibro')

# Campo para ingresar la clave API de OpenAI
api_key = st.text_input("Ingresa tu clave API de OpenAI", type="password")

# Carga de archivos PDF
uploaded_file = st.file_uploader("Sube tu archivo PDF aquí", type=['pdf'])

# Botón para iniciar la conversión
if st.button('Convertir a Audiolibro') and uploaded_file and api_key:
    # Extraer texto del PDF
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    
    # Convertir texto a audio
    audio_data = text_to_speech(text, api_key)
    
    # Convertir los datos de audio a un objeto AudioSegment
    audio_segment = AudioSegment.from_file(BytesIO(audio_data), format="mp3")
    
    # Exportar el objeto AudioSegment a un buffer de bytes
    audio_buffer = BytesIO()
    audio_segment.export(audio_buffer, format="mp3")
    audio_buffer.seek(0)
    
    # Mostrar el reproductor de audio
    st.audio(audio_buffer)
    
    # Botón de descarga para el archivo MP3
    st.download_button(
        label="Descargar Audiolibro",
        data=audio_buffer,
        file_name="audiolibro.mp3",
        mime="audio/mp3"
    )
