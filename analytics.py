import json
from datetime import datetime

analytics_data = {}

def reset():

    analytics_data.clear()

    analytics_data["timestamp"] = str(
        datetime.now()
    )

    analytics_data["customers"] = []

def add_customer(customer):

    analytics_data["customers"].append(
        customer
    )

def save():

    analytics_data["people_count"] = len(
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