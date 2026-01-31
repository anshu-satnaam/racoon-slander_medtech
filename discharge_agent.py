from agent_state import get_state, set_state
from notify import notify_doctor

def discharge_patient(patient_id, doctor_approved):
    stable = get_state(patient_id, "stable")

    if not stable:
        return "Patient not stable for discharge"

    if not doctor_approved:
        return "Waiting for doctor approval"

    set_state(patient_id, "discharged", True)
    notify_doctor(f"Patient {patient_id} discharged successfully")

    return "Patient discharged"
