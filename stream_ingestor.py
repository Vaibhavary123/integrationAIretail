import cv2

CAMERAS = {

    "entrance":
    "videos/shop.mp4",

    "aisle":
    "videos/shop copy.mp4"

    # Replace later with RTSP URLs
}

def get_streams():

    streams = {}

    for name, source in CAMERAS.items():

        streams[name] = cv2.VideoCapture(source)

    return streams  