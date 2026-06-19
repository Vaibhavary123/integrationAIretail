import json


def analyze_queue():

    with open(
        "analytics.json",
        "r"
    ) as f:

        data = json.load(
            f
        )

    people_count = data["people_count"]

    if people_count > 20:

        return (
            "High crowd detected. "
            "Consider opening another counter."
        )

    return (
        "Queue levels are normal."
    )