import json
from datetime import datetime

analytics_data = {}

def reset():

    analytics_data.clear()

    analytics_data["timestamp"] = str(
        datetime.now()
    )

    analytics_data["people_count"] = 0

    analytics_data["customers"] = []

    analytics_data["zone_summary"] = {}

def add_customer(customer):

    analytics_data["customers"].append(
        customer
    )

def update_zone_summary(customers):

    zone_counts = {}

    for customer in customers:

        zone = customer["current_zone"]

        if zone not in zone_counts:

            zone_counts[zone] = 0

        zone_counts[zone] += 1

    analytics_data["zone_summary"] = zone_counts

def save():

    analytics_data["people_count"] = len(
        analytics_data["customers"]
    )

    update_zone_summary(
        analytics_data["customers"]
    )

    with open(
        "analytics.json",
        "w"
    ) as f:

        json.dump(
            analytics_data,
            f,
            indent=4
        )