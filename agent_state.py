# simple in-memory state (later DB)

patient_state = {}

def set_state(patient_id, key, value):
    if patient_id not in patient_state:
        patient_state[patient_id] = {}
    patient_state[patient_id][key] = value

def get_state(patient_id, key):
    return patient_state.get(patient_id, {}).get(key)
