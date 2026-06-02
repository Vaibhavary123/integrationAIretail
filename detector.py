from ultralytics import YOLO
import supervision as sv

model = YOLO(
    "models/yolov8s.onnx",
    task="detect"
)

def detect_people(frame):

    results = model(
        frame,
        imgsz=320,
        conf=0.3,
        verbose=False
    )[0]

    detections = sv.Detections.from_ultralytics(
        results
    )

    detections = detections[
        detections.class_id == 0
    ]

    return detections