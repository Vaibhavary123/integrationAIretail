import cv2

from memory import customer_memory
from analytics import add_customer
from zones import ZONES


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

                "last_zone": None

            }

        memory = customer_memory[track_id]

        # =====================================
        # TOTAL TIME IN STORE
        # =====================================

        memory["frames_seen"] += 1

        # =====================================
        # FIND CURRENT ZONE
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
        # SIMPLE PICKUP DETECTION
        # =====================================

        if current_zone != "walking":

            memory["shelf_frames"] += 1

        else:

            # customer left shelf area

            if memory["shelf_frames"] > 40:

                memory["pickups"] += 1

                memory["picked_item"] = True

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

        add_customer({

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

            "pickups":
            int(memory["pickups"])

        })