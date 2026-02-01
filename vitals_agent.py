from agent_state import set_state
import random

def monitor_vitals(patient_id: str):
    vitals = {
        "heart_rate": random.randint(70, 130),
        "spo2": random.randint(88, 99),
        "temperature": round(random.uniform(36.5, 39.5), 1),
        "bp": "120/80"
    }

    set_state(patient_id, "latest_vitals", vitals)
    return vitals
