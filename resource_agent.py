from agent_state import set_state, get_state

# Initial inventory (can later come from DB)
RESOURCE_INVENTORY = {
    "ICU_beds": 10,
    "Ventilators": 5,
    "Blood_units": 20,
    "Emergency_kits": 8,
    "Oxygen_cylinders": 15
}

# Minimum safe thresholds
MINIMUM_REQUIRED = {
    "ICU_beds": 3,
    "Ventilators": 2,
    "Blood_units": 5,
    "Emergency_kits": 3,
    "Oxygen_cylinders": 5
}

def get_resource_status():
    alerts = []

    for resource, qty in RESOURCE_INVENTORY.items():
        min_required = MINIMUM_REQUIRED[resource]

        if qty < min_required:
            alerts.append({
                "resource": resource,
                "available": qty,
                "minimum_required": min_required,
                "status": "LOW"
            })

    set_state("ADMIN", "resource_alerts", alerts)

    return {
        "inventory": RESOURCE_INVENTORY,
        "alerts": alerts
    }


def consume_resource(resource_name: str, count: int = 1):
    if resource_name in RESOURCE_INVENTORY:
        RESOURCE_INVENTORY[resource_name] = max(
            0, RESOURCE_INVENTORY[resource_name] - count
        )
