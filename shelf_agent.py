import json


def analyze_shelf():

    with open(
        "analytics.json",
        "r"
    ) as f:

        data = json.load(
            f
        )

    people_count = data["people_count"]

    customers = data["customers"]

    pickup_count = 0

    for customer in customers:

        if customer["picked_item"]:

            pickup_count += 1

    if people_count == 0:

        return "No visitors."

    conversion = pickup_count / people_count

    if conversion < 0.2:

        return (
            "Shelf engagement is low. "
            "Consider moving products "
            "closer to beverages or checkout."
        )

    return (
        "Shelf performance looks healthy."
    )