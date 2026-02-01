from pydantic import BaseModel
from typing import Optional, Dict

# -------------------------
# Patient Intake
# -------------------------
class Vitals(BaseModel):
    heart_rate: int
    spo2: int
    temperature: float

class Symptoms(BaseModel):
    chest_pain: bool

class PatientIntakeRequest(BaseModel):
    patient_id: str
    vitals: Vitals
    symptoms: Symptoms

class PatientIntakeResponse(BaseModel):
    patient_id: str
    risk_score: int
    care_path: str
    monitoring_minutes: int
    capacity_status: str


# -------------------------
# Doctor Report
# -------------------------
class ReportRequest(BaseModel):
    patient_id: str
    report: str


# -------------------------
# Surgical Decision
# -------------------------
class SurgicalDecisionRequest(BaseModel):
    patient_id: str
    is_surgical: bool


# -------------------------
# Nurse Instructions
# -------------------------
class NurseInstructionRequest(BaseModel):
    patient_id: str
    doctor_approved: bool


# -------------------------
# Monitor / Stability
# -------------------------
class PatientID(BaseModel):
    patient_id: str


# -------------------------
# Discharge
# -------------------------
class DischargeRequest(BaseModel):
    patient_id: str
    doctor_approved: bool
