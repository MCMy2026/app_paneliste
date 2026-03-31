import pandas as pd

def load_data():
    df = pd.read_csv("data/Base_paneliste.csv")
    df.columns = df.columns.str.lower().str.strip()
    return df