import cv2
from memory import customer_memory

def process_behavior(
    frame,
    tracks,
    shelf_zone
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
                "shelf_time":0,
                "score":0

            }

        memory = customer_memory[track_id]

        memory["frames_seen"] += 1

        inside = cv2.pointPolygonTest(
            shelf_zone,
            (cx,cy),
            False
        )

        action = "Walking"

        if inside >= 0:

            action = "Browsing"

            memory["shelf_time"] += 1

        if memory["shelf_time"] > 50:

            memory["score"] += 1

            memory["shelf_time"] = 0

        if memory["score"] >= 3:

            action = "Suspicious"

        color = (0,255,0)

        if action == "Suspicious":

            color = (0,0,255)

        cv2.rectangle(
            frame,
            (x1,y1),
            (x2,y2),
            color,
            2
        )

        cv2.putText(
            frame,
            f"ID {track_id}",
            (x1,y1-40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            color,
            2
        )

        cv2.putText(
            frame,
            action,
            (x1,y1-15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,255),
            2
        )

        cv2.putText(
            frame,
            f"Score:{memory['score']}",
            (x1,y2+20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255,255,0),
            2
        )