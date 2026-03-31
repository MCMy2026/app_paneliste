import pandas as pd

def load_data():
    try:
        df = pd.read_csv("data/Base_paneliste.csv", encoding="utf-8")
    except:
        df = pd.read_csv("data/Base_paneliste.csv", encoding="latin-1", sep=";")

    # Nettoyage colonnes
    df.columns = df.columns.str.lower().str.strip()

    # 🔥 mapping intelligent
    rename_map = {}

    for col in df.columns:
        if "commune" in col:
            rename_map[col] = "commune"
        if "sexe" in col:
            rename_map[col] = "sexe"
        if "age" in col:
            rename_map[col] = "age"
        if "instruction" in col:
            rename_map[col] = "instruction"
        if "id" in col:
            rename_map[col] = "id"

    df = df.rename(columns=rename_map)

    return df