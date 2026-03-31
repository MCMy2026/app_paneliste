import streamlit as st

st.title("📋 Saisie des appels")

status = st.selectbox("Statut", ["Succès", "Échec", "Rappel"])

if st.button("Valider"):
    st.success("Appel enregistré")