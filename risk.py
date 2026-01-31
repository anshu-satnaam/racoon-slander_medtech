from who_agent import get_thresholds

def calculate_risk(vitals, symptoms):
    thresholds = get_thresholds()
    score = 0

    if vitals["spo2"] < thresholds["spo2_low"]:
        score += 30

    if vitals["heart_rate"] > thresholds["heart_rate_high"]:
        score += 20

    if vitals.get("temperature", 0) > thresholds["temperature_high"]:
        score += 10

    if symptoms.get("chest_pain"):
        score += 20

    return min(score, 100)
