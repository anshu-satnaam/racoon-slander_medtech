from agent_state import get_state, set_state
from notify import notify_doctor

def check_stability(patient_id):
    vitals = get_state(patient_id, "latest_vitals")

    if not vitals:
        return {"stable": False, "reason": "No vitals data"}

    stable = (
        vitals["spo2"] >= 94 and
        vitals["heart_rate"] <= 100 and
        vitals["temperature"] <= 37.5
    )

    set_state(patient_id, "stable", stable)

    if stable:
        notify_doctor(f"Patient {patient_id} appears stable")
    else:
        notify_doctor(f"Patient {patient_id} NOT stable: {vitals}")

    return {
        "stable": stable,
        "vitals": vitals
    }
