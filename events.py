import json
from datetime import datetime

events = []


def add_event(event_type, customer_id, details=None):

    event = {

        "timestamp": str(
            datetime.now()
        ),

        "event_type":
        event_type,

        "customer_id":
        int(customer_id),

        "details":
        details or {}

    }

    events.append(
        event
    )


def save_events():

    with open(
            "events.json",
            "w") as f:

        json.dump(
            events,
            f,
            indent=4
        )