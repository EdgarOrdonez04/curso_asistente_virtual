import streamlit as st

st.title("Multiplicador de numeros")
num = st.text_input("Dame el primer número")
num2 = st.text_input("Dame el segundo número")
r= num * num2
st.write("El resultado de la multiplicación es: ", r)
