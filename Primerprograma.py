import streamlit as st

st.title("Multiplicación de numeros")
num1 = st.input("Dame el primer numero")
num2 = st.input("Dame el segundo numero")
resultado=num1 * num2
st.print("El Resultado es: {resultado}")
