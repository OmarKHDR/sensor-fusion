import cv2
import matplotlib.pyplot as plt
import requests
import signal, sys


def interrupt_handler(signum, frame):
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, interrupt_handler)

cam_url = "http://192.168.1.8:4747/video"

cap = cv2.VideoCapture(cam_url)

