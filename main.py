from fastapi import FastAPI

from risk import calculate_risk
from decision_agent import care_path
from monitor import vitals_interval
from llm_agent import analyze_medical_report
from notify import notify_doctor, notify_nurse
from surgical_agent import surgical_path
from agent_state import set_state, get_state
from vitals_agent import monitor_vitals
from stability_agent import check_stability
from discharge_agent import discharge_patient
from scheduler_agent import start_scheduler
from handoff_agent import handoff_patient
from who_agent import fetch_who_thresholds, get_thresholds


from capacity_agent import (
    admit_patient,
    release_patient,
    nurse_load_status,
    capacity_snapshot
)

app = FastAPI(title="Agentic Hospital AI")


# 1️⃣ Patient Intake

@app.post("/patient/intake")
def patient_intake(data: dict):
    patient_id = data["patient_id"]
    vitals = data["vitals"]
    symptoms = data["symptoms"]

    # Risk + care decision
    risk = calculate_risk(vitals, symptoms)
    path = care_path(risk)
    interval = vitals_interval(risk)

    # Store state
    set_state(patient_id, "risk", risk)
    set_state(patient_id, "care_path", path)

    # Capacity check
    capacity_status = admit_patient(patient_id)

    # Start monitoring ONLY if admitted
    if capacity_status == "ADMITTED":
        start_scheduler(patient_id)

    # Immediate escalation
    if path == "IMMEDIATE":
        notify_doctor(f"Immediate escalation required for patient {patient_id}")
        notify_nurse(f"Prepare emergency care for patient {patient_id}")

    return {
        "patient_id": patient_id,
        "risk_score": risk,
        "care_path": path,
        "monitoring_minutes": interval,
        "capacity_status": capacity_status
    }



# 2️⃣ Doctor uploads report

@app.post("/patient/report")
def report_analysis(data: dict):
    patient_id = data["patient_id"]
    report = data["report"]

    insights = analyze_medical_report(report)
    set_state(patient_id, "report_insights", insights)

    notify_doctor(f"AI Insights for {patient_id}:\n{insights}")

    return {
        "patient_id": patient_id,
        "ai_insights": insights
    }



# 3️⃣ Doctor decides Surgical / Non-Surgical

@app.post("/patient/surgical-decision")
def surgical_decision(data: dict):
    patient_id = data["patient_id"]
    is_surgical = data["is_surgical"]

    decision = surgical_path(is_surgical)
    set_state(patient_id, "surgical", decision)

    notify_doctor(f"Surgical decision for {patient_id}: {decision}")

    return {
        "patient_id": patient_id,
        "decision": decision
    }



# 4️⃣ Nurse instructions (Doctor approval required)

@app.post("/patient/nurse-instructions")
def nurse_instructions(data: dict):
    patient_id = data["patient_id"]
    approved = data["doctor_approved"]

    if not approved:
        return {
            "patient_id": patient_id,
            "status": "Waiting for doctor approval"
        }

    surgical = get_state(patient_id, "surgical")

    if surgical == "SURGICAL":
        instruction = "Pre-op vitals every 15 min, prepare OT, keep patient NPO"
    else:
        instruction = "Medication monitoring, vitals every 30 min"

    notify_nurse(f"Nurse instructions for {patient_id}: {instruction}")

    return {
        "patient_id": patient_id,
        "nurse_instruction": instruction
    }



# 5️⃣ Manual vitals monitoring (optional trigger)

@app.post("/patient/monitor")
def auto_monitor(data: dict):
    patient_id = data["patient_id"]

    vitals = monitor_vitals(patient_id)

    return {
        "patient_id": patient_id,
        "latest_vitals": vitals
    }



# 6️⃣ Stability check

@app.post("/patient/stability")
def patient_stability(data: dict):
    patient_id = data["patient_id"]
    return check_stability(patient_id)



# 7️⃣ Discharge decision

@app.post("/patient/discharge")
def patient_discharge(data: dict):
    patient_id = data["patient_id"]
    approved = data["doctor_approved"]

    result = discharge_patient(patient_id, approved)

    # Release bed ONLY if discharged
    if result == "Patient discharged":
        release_patient(patient_id)

    return {
        "patient_id": patient_id,
        "status": result
    }



@app.get("/hospital/capacity")
def hospital_capacity():
    return {
        "capacity": capacity_snapshot(),
        "nurse_load": nurse_load_status()
    }



# 9️⃣ Patient handoff (department + nurse assignment)
@app.post("/patient/handoff")
def patient_handoff(data: dict):
    patient_id = data["patient_id"]

    care_path = get_state(patient_id, "care_path")
    surgical = get_state(patient_id, "surgical")

    result = handoff_patient(
        patient_id=patient_id,
        care_path=care_path,
        surgical_decision=surgical
    )

    return {
        "patient_id": patient_id,
        "handoff": result
    }

# 🔟 WHO thresholds status / refresh
@app.get("/who/thresholds")
def who_thresholds():
    return get_thresholds()

@app.post("/who/refresh")
def refresh_who():
    return fetch_who_thresholds()
