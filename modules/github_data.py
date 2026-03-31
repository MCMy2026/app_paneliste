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
# FONCTION — LECTURE + NETTOYAGE
# ==========================

def read_data():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    r = requests.get(url, headers=HEADERS)

    # Vérification de l'accès GitHub
    if r.status_code != 200:
        st.error(f"❌ Erreur lecture GitHub (code {r.status_code})")

        if r.status_code == 404:
            st.error("📄 Le fichier existe sur GitHub mais le TOKEN n'a pas la permission 'contents: read'.")
        elif r.status_code == 401:
            st.error("🔑 TOKEN invalide, expiré ou mal configuré.")
        elif r.status_code == 403:
            st.error("⛔ Limite API atteinte ou accès refusé.")

        st.stop()

    data = r.json()

    # Décodage UTF-8 sécurisé
    try:
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
    except Exception as e:
        st.error(f"❌ Erreur décodage Base64 : {e}")
        st.stop()

    # Nettoyage lignes vides + caractères parasites
    content = content.replace("\ufeff", "").strip()

    # Lecture CSV robuste
    try:
        df = pd.read_csv(
            StringIO(content),
            sep=",",
            encoding="utf-8",
            on_bad_lines="skip"
        )
    except Exception as e:
        st.error(f"❌ Erreur lecture du CSV : {e}")
        st.stop()

    # Nouvelle étape : nettoyage auto
    df = clean_dataframe(df)

    return df, data["sha"]


# ==========================
# FONCTION — NETTOYAGE AUTOMATIQUE DU CSV
# ==========================

def clean_dataframe(df):
    # Supprimer espaces cachés
    for col in df.columns:
        try:
            df[col] = df[col].astype(str).str.strip()
        except:
            pass

    # Conversion automatique des colonnes numériques
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    # Suppression lignes totalement vides
    df = df.dropna(how="all")

    return df


# ==========================
# FONCTION — SAUVEGARDE
# ==========================

def save_data(df, sha, max_retries=3):
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

    for _ in range(max_retries):

        # Conversion en CSV
        content = df.to_csv(index=False)
        content_encoded = base64.b64encode(content.encode()).decode()

        payload = {
            "message": "Update data",
            "content": content_encoded,
            "sha": sha
        }

        r = requests.put(url, json=payload, headers=HEADERS)

        if r.status_code in [200, 201]:
            return True

        # Conflit SHA → recharger version GitHub
        if r.status_code == 409:
            time.sleep(1)
            df, sha = read_data()
            continue

        # Autre erreur
        st.error(f"❌ Erreur sauvegarde GitHub (code {r.status_code})")
        return False

    return False


# ==========================
# FONCTION — AJOUT D’UNE LIGNE
# ==========================

def add_row_safe(row):
    df, sha = read_data()
    df = pd.concat([df, pd.DataFrame([row], columns=df.columns)])
    return save_data(df, sha)