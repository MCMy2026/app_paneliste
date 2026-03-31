import pandas as pd

def normalize_sexe(df):
    df["sexe"] = df["sexe"].astype(str).str.lower().str.strip()

    df["sexe"] = df["sexe"].replace({
        "homme": "H",
        "masculin": "H",
        "m": "H",
        "h": "H",
        "femme": "F",
        "feminin": "F",
        "f": "F"
    })

    return df


def safe_sample(df, n):
    if len(df) == 0:
        return pd.DataFrame()
    return df.sample(min(len(df), n), replace=len(df) < n)


def generate_daily(df, commune):

    df = normalize_sexe(df)

    df_c = df[df["commune"] == commune]

    hommes_df = df_c[df_c["sexe"] == "H"]
    femmes_df = df_c[df_c["sexe"] == "F"]

    hommes = safe_sample(hommes_df, 8)
    femmes = safe_sample(femmes_df, 7)

    df_q = pd.concat([hommes, femmes])

    # 🔁 Mélange
    df_q = df_q.sample(frac=1)

    # 👩‍💼 répartition enquêtrices
    enquetrices = ["A", "B", "C"]
    df_q["enquêtrice"] = [enquetrices[i % 3] for i in range(len(df_q))]

    return df_q