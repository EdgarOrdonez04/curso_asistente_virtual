import streamlit as st
from openai import OpenAI
from pathlib import Path

# Sidebar con información
st.sidebar.title("💬 La Vieja Confiable AV")
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Escudo_UACH.svg/1200px-Escudo_UACH.svg.png")
st.sidebar.write("Asistente elaborado por Edgar Francisco Ordoñez Bencomo")

# Obtener la API key desde el archivo .streamlit/secrets.toml
openai_api_key = st.secrets["api_key"]

# Leer archivos del repositorio local
contexto_path = Path("contexto.csv")
referencia_path = Path("negocios.pdf")  # Ejemplo: otro archivo con información a la que se debe apegar

contexto = contexto_path.read_text(encoding="utf-8") if contexto_path.exists() else "Archivo de contexto no encontrado."
referencia = referencia_path.read_text(encoding="utf-8") if referencia_path.exists() else "Archivo de referencia no encontrado."

st.sidebar.subheader("Contexto:")
st.sidebar.code(contexto, language="text")

# Crear cliente OpenAI
client = OpenAI(api_key=openai_api_key)

# Inicializar mensajes de sesión
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": f"Este asistente debe comportarse según el siguiente contexto:\n{contexto}\n\nY debe seguir las siguientes referencias:\n{referencia}"}
    ]

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
if prompt := st.chat_input("Platiquemos"):
    # Agregar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Solicitar respuesta al modelo
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        stream=True,
    )

    # Mostrar respuesta en tiempo real
    with st.chat_message("assistant"):
        response = st.write_stream(stream)

    # Guardar respuesta
    st.session_state.messages.append({"role": "assistant", "content": response})
