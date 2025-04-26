import cv2
from pathlib import Path
import sys
import json


def init_camera():
    global cap
    with open(Path(__file__).parent.parent / "env_var.json") as j:
        obj = json.load(j)
        cam_url = obj["cam_url"]
        print(f"camera index {cam_url}, of type {type(cam_url)}")

    cap = cv2.VideoCapture(cam_url)
    if not cap.isOpened():
        print(f"Could not open camera at {cam_url}")

        for device in [0, 1, 2, 3, 4]:
            print(f"Trying /dev/video{device}")
            cap = cv2.VideoCapture(device)
            if cap.isOpened():
                print(f"Successfully opened /dev/video{device}")
                return cap
        print("Could not open any camera")
        return False
    return cap

if __name__ == '__main__':
    if not init_camera():
        sys.exit(1)

