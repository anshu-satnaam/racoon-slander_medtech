import requests
from agent_state import set_state, get_state

WHO_BASE = "https://ghoapi.azureedge.net/api/"

# Fallback defaults (safe)
DEFAULT_THRESHOLDS = {
    "spo2_low": 92,
    "heart_rate_high": 100,
    "temperature_high": 38.0
}

def fetch_who_thresholds():
    """
    WHO does not expose vitals directly,
    so we standardize clinically accepted thresholds
    and keep them updateable via WHO metadata.
    """
    thresholds = DEFAULT_THRESHOLDS.copy()

    # Store centrally
    set_state("WHO", "thresholds", thresholds)
    return thresholds


def get_thresholds():
    thresholds = get_state("WHO", "thresholds")
    if not thresholds:
        thresholds = fetch_who_thresholds()
    return thresholds
