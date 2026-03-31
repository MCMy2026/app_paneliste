import pandas as pd
import random

def generate_daily(df, commune):

    df_c = df[df["commune"] == commune]

    hommes = df_c[df_c["sexe"] == "H"].sample(8, replace=True)
    femmes = df_c[df_c["sexe"] == "F"].sample(7, replace=True)

    df_q = pd.concat([hommes, femmes]).sample(frac=1)

    df_q["enquêtrice"] = ["A", "B", "C"] * 5

    return df_q.head(15)