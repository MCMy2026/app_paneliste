import pandas as pd
from datetime import datetime
import os

FILE = "data/appels.csv"

def save_call(data):
    df_new = pd.DataFrame([data])

    if os.path.exists(FILE):
        df = pd.read_csv(FILE)
        df = pd.concat([df, df_new], ignore_index=True)
    else:
        df = df_new

    df.to_csv(FILE, index=False)


def load_calls():
    if os.path.exists(FILE):
        return pd.read_csv(FILE)
    return pd.DataFrame()