import cv2

from stream_ingestor import get_streams
from detector import detect_people
from tracker import track_people
from behavior import process_behavior
from analytics import reset, save
from zones import SHELF_ZONE

print("Starting Retail AI...")

# ==========================================
# LOAD STREAMS
# ==========================================

streams = get_streams()

print("Streams Loaded")

# ==========================================
# MAIN LOOP
# ==========================================

while True:

    reset()

    for camera_name, cap in streams.items():

        print(f"\nProcessing {camera_name}")

        # ----------------------------------
        # READ FRAME
        # ----------------------------------

        ret, frame = cap.read()

        print("Frame Read:", ret)

        if not ret:
            continue

        # ----------------------------------
        # RESIZE
        # ----------------------------------

        frame = cv2.resize(
            frame,
            (640, 360)
        )

        # ----------------------------------
        # DETECTION
        # ----------------------------------

        print("Running Detection...")

        detections = detect_people(
            frame
        )

        print(
            "Detections:",
            len(detections)
        )

        # ----------------------------------
        # TRACKING
        # ----------------------------------

        print("Running Tracking...")

        tracks = track_people(
            detections,
            frame,
            camera_name
        )

        print(
            "Tracks:",
            len(tracks)
        )

        # ----------------------------------
        # BEHAVIOR
        # ----------------------------------

        print("Running Behavior...")

        process_behavior(
            tracks,
            SHELF_ZONE
        )

        # ----------------------------------
        # DRAW TRACKS
        # ----------------------------------

        for track in tracks:

            if not track.is_confirmed():
                continue

            x1, y1, x2, y2 = map(
                int,
                track.to_ltrb()
            )

            track_id = track.track_id

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"ID {track_id}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

        # ----------------------------------
        # DRAW SHELF ZONE
        # ----------------------------------

        cv2.polylines(
            frame,
            [SHELF_ZONE],
            True,
            (255, 0, 0),
            2
        )

        # ----------------------------------
        # SHOW
        # ----------------------------------

        cv2.imshow(
            camera_name,
            frame
        )

    save()

    key = cv2.waitKey(1)

    if key == 27:
        break

# ==========================================
# CLEANUP
# ==========================================

for cap in streams.values():

    cap.release()

cv2.destroyAllWindows()