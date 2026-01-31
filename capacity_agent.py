from agent_state import set_state, get_state
from notify import notify_doctor

# Initial hospital capacity (mock)
hospital_capacity = {
    "total_beds": 50,
    "occupied_beds": 0,
    "total_nurses": 20,
    "active_patients": 0
}

def admit_patient(patient_id):
    if hospital_capacity["occupied_beds"] >= hospital_capacity["total_beds"]:
        notify_doctor("No beds available. Consider transfer or delay.")
        return "NO_BED_AVAILABLE"

    hospital_capacity["occupied_beds"] += 1
    hospital_capacity["active_patients"] += 1
    set_state(patient_id, "admitted", True)

    return "ADMITTED"


def release_patient(patient_id):
    hospital_capacity["occupied_beds"] -= 1
    hospital_capacity["active_patients"] -= 1
    set_state(patient_id, "admitted", False)

    return "RELEASED"


def nurse_load_status():
    ratio = hospital_capacity["active_patients"] / hospital_capacity["total_nurses"]

    if ratio > 5:
        notify_doctor("Nurse overload detected")
        return "OVERLOADED"

    return "NORMAL"


def capacity_snapshot():
    return hospital_capacity
