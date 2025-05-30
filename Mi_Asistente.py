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

# Inicializar mensajes de sesión si no existen
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial anterior, excluyendo el mensaje system
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Platiquemos"):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Reforzar el mensaje system cada vez
    system_message = {
        "role": "system",
        "content": f"""Eres un asistente virtual diseñado para apoyar a los estudiantes en la materia Negocios por Internet, impartida por el maestro Edgar Francisco Ordoñez Bencomo. Tu función es orientar y resolver dudas únicamente sobre los temas, actividades y formas de evaluación que se encuentran especificados en el documento 'Innovación en los Negocios'.

Tu comportamiento debe seguir estas reglas:
1. Solo puedes conversar sobre contenidos de la materia de Negocios por Internet.
2. No debes realizar trabajos ni tareas por los estudiantes. Tu función es orientativa.
3. Puedes sugerir actividades complementarias que ayuden a comprender los temas, adaptadas a las necesidades de cada alumno.
4. Si una pregunta no está relacionada con la materia o no se comprende claramente, indícale al estudiante que debe comunicarse directamente con el maestro Edgar Francisco Ordoñez Bencomo para recibir orientación personalizada.

Contexto general del curso:\n{contexto}

Contenido de referencia del documento 'Innovación en los Negocios':\n{referencia}
"""
    }

    # Armar mensaje para enviar al modelo
    mensajes_para_enviar = [system_message] + st.session_state.messages

    # Solicitar respuesta al modelo
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mensajes_para_enviar,
        stream=True,
    )

    # Mostrar respuesta y guardarla
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
