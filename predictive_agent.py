import numpy as np
from agent_state import set_state

def predict_deterioration(patient_id: str, vitals: dict):
    """
    Simple heuristic-based predictor.
    Can be replaced later by trained ML model.
    """

    score = 0

    if vitals["spo2"] < 92:
        score += 0.4
    if vitals["heart_rate"] > 110:
        score += 0.3
    if vitals["temperature"] > 38:
        score += 0.2

    probability = min(score, 1.0)

    risk_level = (
        "HIGH" if probability >= 0.7
        else "MEDIUM" if probability >= 0.4
        else "LOW"
    )

    result = {
        "deterioration_probability": round(probability, 2),
        "risk_level": risk_level
    }

    set_state(patient_id, "predictive_risk", result)

    return result
