from llm_agent import analyze_medical_report
from hospital_structure import DEPARTMENTS
from agent_state import set_state

def recommend_department_and_resources(patient_id, report_text):
    prompt = f"""
    Based on the following medical report,
    recommend:
    1. Department (choose from {list(DEPARTMENTS.keys())})
    2. Doctor role
    3. Resources required

    Report:
    {report_text}
    """

    recommendation = analyze_medical_report(prompt)

    set_state(patient_id, "llm_recommendation", recommendation)

    return recommendation
