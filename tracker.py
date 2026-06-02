from deep_sort_realtime.deepsort_tracker import DeepSort

trackers = {}

def get_tracker(cam_id):

    if cam_id not in trackers:

        trackers[cam_id] = DeepSort(
            max_age=30,
            n_init=2,
            max_cosine_distance=0.3
        )

    return trackers[cam_id]


def track_people(
    detections,
    frame,
    cam_id
):

    tracker = get_tracker(cam_id)

    detection_list = []

    for i in range(len(detections.xyxy)):

        x1, y1, x2, y2 = detections.xyxy[i]

        conf = detections.confidence[i]

        detection_list.append([
            [x1, y1, x2 - x1, y2 - y1],
            conf,
            "person"
        ])

    tracks = tracker.update_tracks(
        detection_list,
        frame=frame
    )

    return tracks