def vitals_interval(risk):
    if risk >= 70:
        return 15
    elif risk >= 40:
        return 30
    else:
        return 60
