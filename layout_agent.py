import json


def analyze_layout():

    with open(
        "analytics.json",
        "r"
    ) as f:

        data = json.load(
            f
        )

    zones = {}

    for customer in data["customers"]:

        zone = customer["most_visited_area"]

        zones[zone] = zones.get(
            zone,
            0
        ) + 1

    if not zones:

        return "No zone data."

    top_zone = max(
        zones,
        key=zones.get
    )

    return (
        f"Highest engagement area is "
        f"{top_zone}. Consider placing "
        f"promotional products there."
    )