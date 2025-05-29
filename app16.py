import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")

openai_api_key = st.secrets["api_key"] 
# Create an OpenAI client.
client = OpenAI(api_key=openai_api_key)

prompt = st.chat_input("¿De que hablaremos hoy?")
if prompt==None:
   st.stop()

with st.chat_message("user", avatar = "🦍"):
   st.markdown(prompt)

# Generate a response using the OpenAI API.
contexto= "eres un experto en asistentes viertuales y ayudas a docentes de la Universidad Autónoma de Chihuahua a crear asistentes para sus cursos virtuales ayudandoles en todo lo posible para implementarlos"
promfinal= contexto + promt
stream = client.chat.completions.create(
        model="gpt-4o-mini",  
        messages=[
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": promptfinal}
        ],
        max_tokens=800,
        temperature=0,
    )
respuesta = stream.choices[0].message.content

with st.chat_message("assistant", avatar = "🗿"):
   st.write(respuesta)
