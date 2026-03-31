import pandas as pd
from datetime import datetime, timedelta
from modules.quotas import apply_quotas
from modules.utils import can_call

def generate_planning(df):
    planning = []
    historique = {}

    start_date = datetime.today()

    communes = df["commune"].unique()

    for day in range(28):
        current_date = start_date + timedelta(days=day)

        for commune in communes:
            df_commune = df[df["commune"] == commune]

            selected = apply_quotas(df_commune)

            for i, row in selected.iterrows():
                id_p = row["id"]

                if can_call(id_p, historique, current_date):

                    enquetrice = ["A", "B", "C"][len(planning) % 3]

                    planning.append({
                        "date": current_date,
                        "commune": commune,
                        "id": id_p,
                        "enquêtrice": enquetrice
                    })

                    historique.setdefault(id_p, []).append(current_date)

    return pd.DataFrame(planning)