import cv2

from memory import customer_memory
from analytics import add_customer

def process_behavior(
    tracks,
    zone
):

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id

        x1,y1,x2,y2 = map(
            int,
            track.to_ltrb()
        )

        cx = (x1+x2)//2
        cy = (y1+y2)//2

        if track_id not in customer_memory:

            customer_memory[track_id] = {

                "frames_seen":0,
                "zone":"walking"

            }

        memory = customer_memory[
            track_id
        ]

        memory["frames_seen"] += 1

        inside = cv2.pointPolygonTest(
            zone,
            (cx,cy),
            False
        )

        if inside >= 0:

            memory["zone"] = "browsing"

        else:

            memory["zone"] = "walking"

        add_customer({

            "customer_id":
            track_id,

            "zone":
            memory["zone"],

            "time_seen":
            memory["frames_seen"]

        })