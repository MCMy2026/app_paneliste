import streamlit as st
from modules.loader import load_data
from modules.planner import generate_planning

st.title("📞 Application PTPC")

if st.button("Générer Planning"):
    df = load_data()
    planning = generate_planning(df)

    st.success("Planning généré !")
    st.dataframe(planning)

    planning.to_excel("planning_ptpc.xlsx", index=False)