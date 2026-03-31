import streamlit as st
from modules.storage import load_calls

st.title("📊 Suivi terrain")

df = load_calls()

if not df.empty:

    total = len(df)
    succes = len(df[df["statut"] == "Succès"])

    st.metric("Total appels", total)
    st.metric("Succès", succes)

    st.progress(succes / total if total > 0 else 0)

    st.dataframe(df.tail(20))

else:
    st.warning("Aucune donnée pour le moment")