import requests
import base64
import pandas as pd
import streamlit as st
from io import StringIO
import time

# ==========================
# CONFIG GITHUB
# ==========================

TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = st.secrets["GITHUB_REPO"]
FILE_PATH = "data/appels_saisis.csv"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


# ==========================
# 1. NETTOYAGE GLOBAL
# ==========================

def clean_dataframe(df):

    # Supprime colonnes sans nom
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df = df.loc[:, df.columns != ""]
    df = df.loc[:, df.columns.notnull()]

    # Strip sur les colonnes texte
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.strip()

    # Convertit les colonnes numériques silencieusement
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # Supprime les lignes vides
    df = df.dropna(how="all")

    # Réinitialise les index
    df = df.reset_index(drop=True)

    return df



# ==========================
# 2. LECTURE CSV (100% ROBUSTE)
# ==========================

EXPECTED_COLS = [
    "Date","Enqueteur","Telephone","Commune",
    "Status","Sexe","Age_group","Niveau_cat"
]

def read_data():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        st.error(f"❌ Erreur lecture GitHub (code {r.status_code})")
        st.stop()

    data = r.json()

    # Décode Base64
    try:
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except Exception as e:
        st.error("❌ Erreur décodage Base64 : " + str(e))
        st.stop()

    # Lecture CSV robuste
    try:
        df = pd.read_csv(StringIO(content), sep=",", encoding="utf-8", on_bad_lines="skip")
    except Exception:
        # Deuxième tentative : parfois les CSV ont un BOM
        df = pd.read_csv(StringIO(content.lstrip("\ufeff")), sep=",", encoding="utf-8", on_bad_lines="skip")

    df = clean_dataframe(df)

    # Ajuste automatiquement si les colonnes sont mauvaises ou manquantes
    # -------------------------------------------------------------------
    if len(df.columns) != len(EXPECTED_COLS):
        st.warning("⚠️ Correction automatique des colonnes du CSV…")
        df = df.reindex(columns=EXPECTED_COLS, fill_value="")

    return df, data["sha"]



# ==========================
# 3. SAUVEGARDE AUTOMATIQUE (ROBUSTE)
# ==========================

def save_data(df, sha, max_retries=5):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

    # Force nettoyage avant sauvegarde
    df = clean_dataframe(df)
    df = df.reindex(columns=EXPECTED_COLS)

    for _ in range(max_retries):

        # Encode CSV → Base64
        content = df.to_csv(index=False)
        content_encoded = base64.b64encode(content.encode()).decode()

        payload = {
            "message": "Auto-update (Streamlit safe write)",
            "content": content_encoded,
            "sha": sha
        }

        r = requests.put(url, json=payload, headers=HEADERS)

        if r.status_code in (200, 201):
            return True

        # Conflit SHA → relecture et nouvelle tentative
        if r.status_code == 409:
            time.sleep(1)
            df, sha = read_data()
            continue

        # Autre erreur
        st.error(f"❌ Erreur GitHub (code {r.status_code})")
        return False

    return False



# ==========================
# 4. AJOUT D’UNE LIGNE (AUTO‑RÉPARATION)
# ==========================

def add_row_safe(row):

    df, sha = read_data()

    # Ajuste automatiquement la taille
    # Si la ligne a moins de 8 valeurs → compléter
    if len(row) < len(EXPECTED_COLS):
        row += [""] * (len(EXPECTED_COLS) - len(row))

    # Si la ligne a trop de valeurs → tronquer
    if len(row) > len(EXPECTED_COLS):
        row = row[:len(EXPECTED_COLS)]

    # Ajoute la ligne en respectant l’ordre des colonnes
    df.loc[len(df)] = row

    return save_data(df, sha)