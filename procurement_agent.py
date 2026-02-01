from email_agent import send_email

FINANCE_EMAIL = "finance@example.com"

def notify_finance(alerts):
    if not alerts:
        return "No procurement needed"

    body = "⚠️ Resource Procurement Alert\n\n"

    for alert in alerts:
        body += (
            f"- {alert['resource']}: "
            f"{alert['available']} available "
            f"(minimum required {alert['minimum_required']})\n"
        )

    body += "\nPlease initiate procurement at the earliest."

    send_email(
        FINANCE_EMAIL,
        "URGENT: Hospital Resource Shortage",
        body
    )

    return "Finance notified"
