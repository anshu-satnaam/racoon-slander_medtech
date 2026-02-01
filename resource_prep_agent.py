from agent_state import get_state
from notify import notify_nurse

def prepare_resources(patient_id, doctor_approved):
    if not doctor_approved:
        return "Waiting for doctor approval"

    recommendation = get_state(patient_id, "llm_recommendation")

    notify_nurse(
        f"Prepare resources for patient {patient_id}:\n{recommendation}"
    )

    return "Resources preparation started"
