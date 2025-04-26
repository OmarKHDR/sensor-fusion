#!/usr/bin/env python3
from detect_obj import detector
from calibration.calibration_samples_gen import generate_calibration_samples
from calibration.calibrate import calibrate_from_samples


while True:
	prog = input("enter c for calibration, d for detection, q to quit: ")
	if prog == 'c':
		print("you can edit checkerboard size in env_var.json file, also the camera uri")
		generate_calibration_samples()
		calibrate_from_samples()
	elif prog == 'd':
		print("you can edit the camera uri from env_var.json file")
		detector()
	elif prog == 'q':
		exit()

