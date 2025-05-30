import streamlit as st
from openai import OpenAI
from pathlib import Path
import fitz  # PyMuPDF para leer PDFs

# Sidebar con información
st.sidebar.title("💬 La Vieja Confiable AV")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Escudo_UACH.svg/1200px-Escudo_UACH.svg.png")
st.sidebar.write("Asistente elaborado por Edgar Francisco Ordoñez Bencomo")

# Obtener la API key desde el archivo .streamlit/secrets.toml
openai_api_key = st.secrets["api_key"]

# Función para leer PDF
def leer_pdf(path):
    try:
        doc = fitz.open(path)
        texto = ""
        for page in doc:
            texto += page.get_text()
        return texto
    except Exception as e:
        return f"Error al leer PDF: {e}"

# Leer archivos locales
contexto_path = Path("contexto.csv")
referencia_path = Path("Negocios.pdf")

contexto = contexto_path.read_text(encoding="utf-8") if contexto_path.exists() else "Archivo de contexto no encontrado."
referencia = leer_pdf(referencia_path) if referencia_path.exists() else "Archivo de referencia no encontrado."

# Crear cliente OpenAI
client = OpenAI(api_key=openai_api_key)

# Inicializar mensajes de sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Instrucciones internas para la IA (no se muestran al usuario)
instrucciones = {
    "role": "system",
    "content": f"Este asistente debe comportarse según el siguiente contexto:\n{contexto}\n\nY debe seguir las siguientes referencias:\n{referencia}"
}

# Asegurar que el mensaje del sistema esté al inicio
if not any(msg["role"] == "system" for msg in st.session_state.messages):
    st.session_state.messages.insert(0, instrucciones)

# Mostrar mensajes previos, excepto el mensaje del sistema
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Platiquemos"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        stream=True,
    )

    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
