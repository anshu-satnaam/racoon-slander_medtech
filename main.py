from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

# =========================================================
# In-memory DB (demo purpose)
# =========================================================
PATIENT_DB = []

# =========================================================
# Core agents
# =========================================================
from risk import calculate_risk
from decision_agent import care_path
from monitor import vitals_interval
from vitals_agent import monitor_vitals
from stability_agent import check_stability
from discharge_agent import discharge_patient
from surgical_agent import surgical_path
from predictive_agent import predict_deterioration
from diagnostic_agent import diagnostic_support

# Intelligence
from llm_agent import analyze_medical_report
from recommendation_agent import recommend_department_and_resources
from post_surgery_agent import post_surgery_monitoring
from handoff_agent import handoff_patient
from scheduler_agent import start_scheduler
from admin_agent import admin_overview

# Ops
from notify import notify_doctor, notify_nurse
from capacity_agent import admit_patient, release_patient, nurse_load_status, capacity_snapshot
from resource_prep_agent import prepare_resources

# External
from who_agent import fetch_who_thresholds, get_thresholds
from email_agent import send_discharge_emails
from calendar_agent import create_followup_event

# State
from agent_state import set_state, get_state

# Schemas
from schemas import (
    PatientIntakeRequest,
    PatientIntakeResponse,
    SurgicalDecisionRequest,
    NurseInstructionRequest,
    PatientID,
    DischargeRequest
)

# =========================================================
# App
# =========================================================
app = FastAPI(title="Agentic Hospital AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # HTML/JS friendly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# 1️⃣ Patient Intake (Vitals based)
# =========================================================
@app.post("/patient/intake", response_model=PatientIntakeResponse)
def patient_intake(data: PatientIntakeRequest):
    risk = calculate_risk(data.vitals.dict(), data.symptoms.dict())
    path = care_path(risk)

    set_state(data.patient_id, "risk", risk)
    set_state(data.patient_id, "care_path", path)

    admit_patient(data.patient_id)

    return {
        "patient_id": data.patient_id,
        "risk_score": risk,
        "care_path": path,
        "monitoring_minutes": vitals_interval(risk),
        "capacity_status": "ADMITTED"
    }

# =========================================================
# 2️⃣ MAIN LLM ENDPOINT (HTML FRONTEND USES THIS)
# =========================================================
@app.post("/patient/report")
def patient_report(patient_id: str = Form(...), report: str = Form(...)):
    insights = analyze_medical_report(report)

    record = {
        "patient_id": patient_id,
        "summary": insights,
        "department": "Cardiology",
        "doctor": "Dr. Sharma",
        "risk_score": 72,
        "status": "UNDER_REVIEW"
    }

    PATIENT_DB.append(record)
    return record

# =========================================================
# 3️⃣ Diagnostic Support (File Upload)
# =========================================================
@app.post("/patient/diagnostic-support")
async def diagnostic_support_endpoint(
    patient_id: str = Form(...),
    file: UploadFile = File(...)
):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    summary = diagnostic_support(patient_id, file_path)

    record = {
        "patient_id": patient_id,
        "summary": summary,
        "department": "General",
        "doctor": "Dr. AI",
        "risk_score": 55,
        "status": "DIAGNOSTIC"
    }

    PATIENT_DB.append(record)
    return record

# =========================================================
# 4️⃣ Get all patients (Admin / Doctor / Nurse panels)
# =========================================================
@app.get("/patients")
def get_patients():
    return PATIENT_DB

# =========================================================
# 5️⃣ Surgical decision
# =========================================================
@app.post("/patient/surgical-decision")
def surgical_decision(data: SurgicalDecisionRequest):
    decision = surgical_path(data.is_surgical)
    set_state(data.patient_id, "surgical", decision)
    return {"patient_id": data.patient_id, "decision": decision}

# =========================================================
# 6️⃣ Nurse instructions
# =========================================================
@app.post("/patient/nurse-instructions")
def nurse_instructions(data: NurseInstructionRequest):
    if not data.doctor_approved:
        return {"status": "BLOCKED"}

    instruction = "Vitals every 30 minutes"
    notify_nurse(instruction)
    return {"instruction": instruction}

# =========================================================
# 7️⃣ Predictive Risk
# =========================================================
@app.post("/patient/predict-risk")
def predictive_risk(patient_id: str):
    vitals = get_state(patient_id, "latest_vitals")
    if not vitals:
        return {"status": "NO_VITALS"}
    return predict_deterioration(patient_id, vitals)

# =========================================================
# 8️⃣ Discharge
# =========================================================
@app.post("/patient/discharge")
def patient_discharge(data: DischargeRequest):
    result = discharge_patient(data.patient_id, data.doctor_approved)
    if result == "Patient discharged":
        release_patient(data.patient_id)
    return {"status": result}

# =========================================================
# 9️⃣ Admin / Ops
# =========================================================
@app.get("/hospital/capacity")
def hospital_capacity():
    return {
        "capacity": capacity_snapshot(),
        "nurse_load": nurse_load_status()
    }

@app.get("/admin/overview")
def admin_dashboard():
    return admin_overview()

# =========================================================
# 10️⃣ WHO
# =========================================================
@app.get("/who/thresholds")
def who_thresholds():
    return get_thresholds()

@app.post("/who/refresh")
def who_refresh():
    return fetch_who_thresholds()
