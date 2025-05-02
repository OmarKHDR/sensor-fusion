#!/usr/bin/env python3
from detect_obj import detector
from calibration.calibration_samples_gen import generate_calibration_samples
from calibration.calibrate import calibrate_from_samples
from calibration.trycamera import init_camera
import cv2
import sys
import signal

def interrupt_handler(signum, frame):
    global cap
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    print("Goodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, interrupt_handler)

while True:
	cap = None
	print("hints: you can edit checkerboard size and the camera uri in [[env_var.json]]")
	print("hints: you can edit object place from [[ultrasonic.json]]")
	prog = input("enter c for calibration, d for detection, q to quit: ")

	if prog == 'c':
		cap = init_camera()
		generate_calibration_samples(cap)
		calibrate_from_samples()
	elif prog == 'd':
		cap = init_camera()
		detector(cap)
	elif prog == 'q':
		exit(0)

