import streamlit as st

st.title("📊 Dashboard")

st.metric("Appels réalisés", 120)
st.metric("Objectif", 210)
st.progress(120/210)