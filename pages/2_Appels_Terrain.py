import streamlit as st
from modules.storage import save_call, load_calls
from datetime import datetime

st.title("📞 Appels Terrain")

# 👤 Identification enquêtrice
enq = st.selectbox("Enquêtrice", ["A", "B", "C"])

# 📍 Infos appel
commune = st.text_input("Commune")
paneliste = st.text_input("ID Panéliste")

# ⏱️ chrono simple
if "start" not in st.session_state:
    st.session_state.start = None

if st.button("▶️ Démarrer"):
    st.session_state.start = datetime.now()

if st.session_state.start:
    duree = (datetime.now() - st.session_state.start).seconds
    st.info(f"⏱️ Durée : {duree} sec")

# 📋 statut
statut = st.radio("Résultat", ["Succès", "Échec", "Rappel"])

# 💾 bouton terrain simple
if st.button("✅ Enregistrer"):
    save_call({
        "date": datetime.now(),
        "enquêtrice": enq,
        "commune": commune,
        "paneliste": paneliste,
        "statut": statut,
        "duree": duree if st.session_state.start else 0
    })

    st.success("✔️ Appel enregistré")

# 📊 historique
st.subheader("Historique récent")
st.dataframe(load_calls().tail(10))