from agent_state import get_all_state
from capacity_agent import capacity_snapshot, nurse_load_status
from resource_agent import get_resource_status

DEPARTMENTS = [
    "Emergency",
    "Surgical",
    "General",
    "Cardiothoracic",
    "Radiology",
    "Pathology"
]

def admin_overview():
    state = get_all_state()

    total_patients = len(state)

    dept_counts = {d: 0 for d in DEPARTMENTS}
    risk_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}

    for patient_id, pdata in state.items():
        dept = pdata.get("department")
        risk = pdata.get("risk", 0)

        if dept in dept_counts:
            dept_counts[dept] += 1

        if risk >= 70:
            risk_counts["HIGH"] += 1
        elif risk >= 40:
            risk_counts["MEDIUM"] += 1
        else:
            risk_counts["LOW"] += 1

    # ✅ FIX: fetch resource status properly
    resources = get_resource_status()

    return {
        "total_patients": total_patients,
        "patients_by_department": dept_counts,
        "risk_distribution": risk_counts,
        "capacity": capacity_snapshot(),
        "nurse_load": nurse_load_status(),
        "resources": resources
    }
