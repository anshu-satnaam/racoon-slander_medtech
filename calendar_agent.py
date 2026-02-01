from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth import get_credentials

def create_followup_event(
    patient_email,
    doctor_email,
    days_after,
    duration_minutes,
    description
):
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    start_time = datetime.utcnow() + timedelta(days=days_after)
    end_time = start_time + timedelta(minutes=duration_minutes)

    event = {
        "summary": "Hospital Follow-up Appointment",
        "description": description,
        "start": {
            "dateTime": start_time.isoformat() + "Z"
        },
        "end": {
            "dateTime": end_time.isoformat() + "Z"
        },
        "attendees": [
            {"email": patient_email},
            {"email": doctor_email}
        ],
        "reminders": {
            "useDefault": True
        }
    }

    service.events().insert(
        calendarId="primary",
        body=event,
        sendUpdates="all"
    ).execute()
