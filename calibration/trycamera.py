import cv2
import matplotlib.pyplot as plt
import signal, sys


def interrupt_handler(signum, frame):
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, interrupt_handler)

cam_url = 0

cap = cv2.VideoCapture(cam_url)

