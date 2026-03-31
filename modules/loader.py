import pandas as pd

def load_data():
    try:
        df = pd.read_csv("data/Base_paneliste.csv", encoding="utf-8")
    except:
        df = pd.read_csv("data/Base_paneliste.csv", encoding="latin-1")

    df.columns = df.columns.str.lower().str.strip()
    return df