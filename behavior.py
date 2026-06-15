import cv2

from memory import customer_memory
from analytics import add_customer
from zones import ZONES
from events import add_event


def process_behavior(tracks):

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id

        x1, y1, x2, y2 = map(
            int,
            track.to_ltrb()
        )

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # =====================================
        # CREATE CUSTOMER MEMORY
        # =====================================

        if track_id not in customer_memory:

            customer_memory[track_id] = {

                "frames_seen": 0,

                "current_zone": "unknown",

                "zones": {

                    zone_name: 0

                    for zone_name in ZONES.keys()

                },

                "picked_item": False,

                "pickups": 0,

                "shelf_frames": 0,

                "last_zone": None,

                "journey": [],

                "positions": []

            }

            add_event(

                "customer_entered",

                track_id

            )

        memory = customer_memory[track_id]

        # =====================================
        # TOTAL TIME
        # =====================================

        memory["frames_seen"] += 1

        # =====================================
        # SAVE POSITION
        # =====================================

        memory["positions"].append(

            (cx, cy)

        )

        if len(memory["positions"]) > 1000:

            memory["positions"].pop(0)

        # =====================================
        # DETERMINE CURRENT ZONE
        # =====================================

        current_zone = "walking"

        for zone_name, zone_poly in ZONES.items():

            inside = cv2.pointPolygonTest(

                zone_poly,

                (cx, cy),

                False

            )

            if inside >= 0:

                current_zone = zone_name

                memory["zones"][zone_name] += 1

                break

        memory["current_zone"] = current_zone

        # =====================================
        # ZONE CHANGE EVENT
        # =====================================

        if current_zone != memory["last_zone"]:

            add_event(

                "zone_changed",

                track_id,

                {

                    "zone": current_zone

                }

            )

            memory["journey"].append(

                current_zone

            )

            memory["last_zone"] = current_zone

        # =====================================
        # PICKUP DETECTION
        # =====================================

        if current_zone != "walking":

            memory["shelf_frames"] += 1

        else:

            if memory["shelf_frames"] > 40:

                memory["pickups"] += 1

                memory["picked_item"] = True

                add_event(

                    "item_pickup",

                    track_id,

                    {

                        "zone": current_zone

                    }

                )

            memory["shelf_frames"] = 0

        # =====================================
        # MOST VISITED AREA
        # =====================================

        most_visited_area = max(

            memory["zones"],

            key=memory["zones"].get

        )

        # =====================================
        # SAVE ANALYTICS
        # =====================================

        add_customer(

            {

                "customer_id":
                int(track_id),

                "time_in_store":
                int(memory["frames_seen"]),

                "current_zone":
                current_zone,

                "most_visited_area":
                most_visited_area,

                "picked_item":
                memory["picked_item"],

                "pickup_count":
                int(memory["pickups"]),

                "journey":
                memory["journey"]

            }

        )