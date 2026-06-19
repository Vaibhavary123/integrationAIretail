import json


def analyze_promotions():

    with open(
        "events.json",
        "r"
    ) as f:

        events = json.load(
            f
        )

    pickups = 0

    for event in events:

        if event["event_type"] == "item_pickup":

            pickups += 1

    if pickups < 5:

        return (
            "Promotional performance is weak. "
            "Consider changing display strategy."
        )

    return (
        "Promotions are performing well."
    )
