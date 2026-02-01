STATE = {}

def set_state(patient_id, key, value):
    if patient_id not in STATE:
        STATE[patient_id] = {}
    STATE[patient_id][key] = value

def get_state(patient_id, key=None):
    if key:
        return STATE.get(patient_id, {}).get(key)
    return STATE.get(patient_id, {})

def get_all_state():
    return STATE
