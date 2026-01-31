def care_path(risk):
    if risk >= 70:
        return "IMMEDIATE"
    elif risk >= 40:
        return "NON_IMMEDIATE"
    else:
        return "LOW_RISK"
