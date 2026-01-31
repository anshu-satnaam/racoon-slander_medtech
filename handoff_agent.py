from agent_state import set_state
from notify import notify_doctor, notify_nurse

# Mock department & nurse pools
DEPARTMENTS = {
    "SURGICAL": "Surgery",
    "NON_SURGICAL": "General Medicine",
    "IMMEDIATE": "Emergency"
}

NURSES = [
    "Nurse A",
    "Nurse B",
    "Nurse C",
    "Nurse D"
]

nurse_index = 0

def assign_nurse():
    global nurse_index
    nurse = NURSES[nurse_index % len(NURSES)]
    nurse_index += 1
    return nurse


def handoff_patient(patient_id, care_path, surgical_decision):
    # Decide department
    if care_path == "IMMEDIATE":
        department = DEPARTMENTS["IMMEDIATE"]
    elif surgical_decision == "SURGICAL":
        department = DEPARTMENTS["SURGICAL"]
    else:
        department = DEPARTMENTS["NON_SURGICAL"]

    nurse = assign_nurse()

    # Save state
    set_state(patient_id, "department", department)
    set_state(patient_id, "assigned_nurse", nurse)

    # Notify
    notify_doctor(
        f"Patient {patient_id} handed off to {department}, Nurse: {nurse}"
    )
    notify_nurse(
        f"You are assigned to patient {patient_id} in {department}"
    )

    return {
        "department": department,
        "nurse": nurse
    }
