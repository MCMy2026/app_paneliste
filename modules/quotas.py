import pandas as pd

def apply_quotas(df):
    hommes = df[df["sexe"] == "H"].sample(8, replace=True)
    femmes = df[df["sexe"] == "F"].sample(7, replace=True)

    df_sexe = pd.concat([hommes, femmes])

    jeunes = df_sexe[df_sexe["age"] <= 39].sample(12, replace=True)
    moyens = df_sexe[(df_sexe["age"] >= 40) & (df_sexe["age"] <= 54)].sample(2, replace=True)
    seniors = df_sexe[df_sexe["age"] >= 55].sample(1, replace=True)

    df_age = pd.concat([jeunes, moyens, seniors])

    bas = df_age[df_age["instruction"] == "inferieur"].sample(12, replace=True)
    sup = df_age[df_age["instruction"] == "superieur"].sample(3, replace=True)

    final = pd.concat([bas, sup])

    return final