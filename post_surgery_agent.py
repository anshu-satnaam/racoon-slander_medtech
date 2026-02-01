from agent_state import set_state
from monitor import vitals_interval

def post_surgery_monitoring(patient_id, surgery_success, risk_score):
    if not surgery_success:
        return "Surgery failed – escalate immediately"

    if risk_score >= 70:
        category = "HIGH_RISK"
    elif risk_score >= 40:
        category = "MEDIUM_RISK"
    else:
        category = "LOW_RISK"

    interval = vitals_interval(risk_score)

    set_state(patient_id, "post_surgery_category", category)
    set_state(patient_id, "monitoring_interval", interval)

    return {
        "category": category,
        "monitoring_interval_minutes": interval
    }
