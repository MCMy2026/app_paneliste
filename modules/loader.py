import pandas as pd

def load_data(path="data/Base_paneliste.csv"):
    df = pd.read_csv(path)

    # Normalisation colonnes
    df.columns = df.columns.str.lower().str.strip()

    return df