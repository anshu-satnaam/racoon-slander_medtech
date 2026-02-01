import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth import get_credentials
from llm_agent import analyze_medical_report

def send_email(to_email: str, subject: str, body: str):
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()


def send_discharge_emails(patient_email, surgery_summary, followup_days):
    # 1️⃣ Feedback form
    feedback_body = analyze_medical_report(
        "Generate a short patient feedback form with 5 questions"
    )

    send_email(
        patient_email,
        "We value your feedback",
        feedback_body
    )

    # 2️⃣ Surgery / procedure summary
    summary_body = analyze_medical_report(
        f"Create a patient-friendly discharge summary:\n{surgery_summary}"
    )

    send_email(
        patient_email,
        "Your Discharge Summary",
        summary_body
    )

    # 3️⃣ Follow-up info
    followup_body = f"Your follow-up appointment is scheduled in {followup_days} days."

    send_email(
        patient_email,
        "Follow-up Appointment",
        followup_body
    )
