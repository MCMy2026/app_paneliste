import streamlit as st
from modules.loader import load_data
from modules.planner import generate_daily

st.title("📅 Planning Journalier")

df = load_data()

commune = st.selectbox("Choisir commune", df["commune"].unique())

if st.button("Générer"):
    planning = generate_daily(df, commune)
    st.dataframe(planning)