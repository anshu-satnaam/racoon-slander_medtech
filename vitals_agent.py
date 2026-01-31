import random
from agent_state import set_state, get_state
from notify import notify_doctor

def generate_vitals():
    return {
        "heart_rate": random.randint(70, 140),
        "spo2": random.randint(85, 99),
        "temperature": round(random.uniform(36.5, 39.5), 1)
    }

def monitor_vitals(patient_id):
    vitals = generate_vitals()
    set_state(patient_id, "latest_vitals", vitals)

    # simple fluctuation detection
    if vitals["spo2"] < 90 or vitals["heart_rate"] > 120:
        notify_doctor(
            f"Vitals unstable for patient {patient_id}: {vitals}"
        )

    return vitals

