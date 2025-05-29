import streamlit as st

st.title("Multiplicador de numeros")
num = st.text_input("Dame el primer número")
numer = st.text_input("Dame el segundo número")
r= num * numer
st.write("El resultado de la multiplicación es: ", r)
