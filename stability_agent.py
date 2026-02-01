from datetime import datetime, timedelta
from agent_state import get_state, set_state

def check_stability(patient_id: str):
    """
    Checks whether patient has remained stable
    for the doctor-defined duration.
    FAIL-SAFE: Never raises exception.
    """

    try:
        # 1️⃣ Fetch required state
        risk = get_state(patient_id, "risk")
        last_vitals = get_state(patient_id, "latest_vitals")
        stable_since = get_state(patient_id, "stable_since")

        # 2️⃣ Validate required data
        if risk is None or last_vitals is None:
            return {
                "status": "INSUFFICIENT_DATA",
                "action": "Continue monitoring"
            }

        # 3️⃣ Define stability thresholds
        is_stable = (
            last_vitals.get("spo2", 0) >= 92 and
            last_vitals.get("heart_rate", 999) <= 100 and
            last_vitals.get("temperature", 99) <= 37.8
        )

        now = datetime.utcnow()

        # 4️⃣ Track stable duration
        if is_stable:
            if not stable_since:
                set_state(patient_id, "stable_since", now)
                return {
                    "status": "STABLE",
                    "stable_duration_met": False
                }

            stable_duration = now - stable_since

            # Doctor-defined time (based on risk)
            required_minutes = (
                60 if risk < 40 else
                30 if risk < 70 else
                15
            )

            if stable_duration >= timedelta(minutes=required_minutes):
                return {
                    "status": "STABLE",
                    "stable_duration_met": True,
                    "recommendation": "Eligible for discharge"
                }

            return {
                "status": "STABLE",
                "stable_duration_met": False
            }

        # 5️⃣ If unstable
        set_state(patient_id, "stable_since", None)

        return {
            "status": "UNSTABLE",
            "action": "Continue monitoring or escalate"
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
