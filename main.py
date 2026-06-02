import cv2

from detector import detect_people
from tracker import track_people
from behavior import process_behavior
from zones import SHELF_ZONE

cap1 = cv2.VideoCapture(
    "videos/shop.mp4"
)

cap2 = cv2.VideoCapture(
    "videos/shop copy.mp4"
)

while True:

    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    frame1 = cv2.resize(
        frame1,
        (640,360)
    )

    frame2 = cv2.resize(
        frame2,
        (640,360)
    )

    detections1 = detect_people(
        frame1
    )

    detections2 = detect_people(
        frame2
    )

    tracks1 = track_people(
        detections1,
        frame1,
        1
    )

    tracks2 = track_people(
        detections2,
        frame2,
        2
    )

    process_behavior(
        frame1,
        tracks1,
        SHELF_ZONE
    )

    process_behavior(
        frame2,
        tracks2,
        SHELF_ZONE
    )

    cv2.polylines(
        frame1,
        [SHELF_ZONE],
        True,
        (255,0,0),
        2
    )

    cv2.polylines(
        frame2,
        [SHELF_ZONE],
        True,
        (255,0,0),
        2
    )

    combined = cv2.hconcat([
        frame1,
        frame2
    ])

    cv2.imshow(
        "Retail AI V2",
        combined
    )

    if cv2.waitKey(1) == 27:
        break

cap1.release()
cap2.release()

cv2.destroyAllWindows()