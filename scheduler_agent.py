import time
import threading
from agent_state import get_state
from vitals_agent import monitor_vitals
from monitor import vitals_interval

def patient_scheduler(patient_id):
    while True:
        risk = get_state(patient_id, "risk")

        if risk is None:
            time.sleep(60)
            continue

        interval = vitals_interval(risk)
        monitor_vitals(patient_id)

        time.sleep(interval * 60)


def start_scheduler(patient_id):
    thread = threading.Thread(
        target=patient_scheduler,
        args=(patient_id,),
        daemon=True
    )
    thread.start()
