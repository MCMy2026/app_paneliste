import requests
import base64
import pandas as pd
import streamlit as st
from io import StringIO
import time

TOKEN = st.secrets["GITHUB_TOKEN"]
REPO = st.secrets["GITHUB_REPO"]
FILE_PATH = "data/appels_saisis.csv"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# =========================
# LECTURE SECURISEE
# =========================
def read_data():
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

    r = requests.get(url, headers=HEADERS)

    if r.status_code != 200:
        st.error("❌ Erreur lecture GitHub")
        st.stop()

    data = r.json()

    content = base64.b64decode(data["content"]).decode("utf-8")
    df = pd.read_csv(StringIO(content))

    return df, data["sha"]

# =========================
# ECRITURE AVEC RETRY
# =========================
def save_data(df, sha, max_retries=3):

    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

    for attempt in range(max_retries):

        content = df.to_csv(index=False)
        content_encoded = base64.b64encode(content.encode()).decode()

        payload = {
            "message": f"Update data (attempt {attempt+1})",
            "content": content_encoded,
            "sha": sha
        }

        r = requests.put(url, json=payload, headers=HEADERS)

        if r.status_code in [200, 201]:
            return True

        elif r.status_code == 409:
            # 🔁 conflit → on recharge et retry
            time.sleep(1)
            df_latest, sha = read_data()

        else:
            st.error(f"❌ Erreur GitHub: {r.status_code}")
            return False

    st.error("❌ Échec après plusieurs tentatives")
    return False

# =========================
# AJOUT LIGNE SAFE
# =========================
def add_row_safe(new_row):

    df, sha = read_data()

    df = pd.concat([df, pd.DataFrame([new_row], columns=df.columns)])

    success = save_data(df, sha)

    return success