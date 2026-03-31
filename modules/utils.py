from datetime import datetime, timedelta

def can_call(paneliste, historique, date):
    # pas 2 jours de suite
    if paneliste in historique:
        last_call = historique[paneliste][-1]
        if (date - last_call).days == 1:
            return False

    # max 2 appels/semaine
    if paneliste in historique:
        last_week = [d for d in historique[paneliste] if (date - d).days <= 7]
        if len(last_week) >= 2:
            return False

    return True