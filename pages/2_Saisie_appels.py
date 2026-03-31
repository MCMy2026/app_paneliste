import streamlit as st
import time

st.title("📋 Saisie des appels")

if "start_time" not in st.session_state:
    st.session_state.start_time = None

if st.button("▶️ Démarrer appel"):
    st.session_state.start_time = time.time()

if st.session_state.start_time:
    duration = int(time.time() - st.session_state.start_time)
    st.info(f"⏱️ Durée : {duration} sec")

statut = st.selectbox("Statut appel", ["Succès", "Échec", "Rappel"])

if st.button("✅ Valider appel"):
    st.success("Appel enregistré !")