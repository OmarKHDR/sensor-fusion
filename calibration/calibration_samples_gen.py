import cv2
import numpy as np
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from calibration.trycamera import init_camera
import os
import json

def generate_calibration_samples():
	with open(Path(__file__).parent.parent / "env_var.json") as j:
		obj = json.load(j)
		CHECKERBOARD = (obj["board"][0], obj["board"][1])
		square_size = obj["square_size"]

	#print(CHECKERBOARD)
	save_path = "calibration/calibration_samples.npz"
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

	objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
	objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
	objp *= square_size

	objpoints = []
	imgpoints = []

	count = 0
	MAX_SAMPLES = 20
	cap = init_camera()
	if not cap:
		print("failed to initialize camera, exiting...")
		exit(1)
	while True:
		ret, frame = cap.read()
		if not ret:
			print("you are a failure")
			continue

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		ret_corners, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)

		if ret_corners:
			corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
			cv2.drawChessboardCorners(frame, CHECKERBOARD, corners2, ret_corners)


		cv2.imshow("Calibration", frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord(' '):  # Spacebar pressed
			if ret_corners:
				objpoints.append(objp)
				imgpoints.append(corners2)
				count += 1
				print(f"[+] Captured frame {count}/{MAX_SAMPLES}")
			else:
				print("[-] Checkerboard not detected. Try again.")

			if count >= MAX_SAMPLES:
				print("Collected enough samples. Calibrating...")
				break
		elif key == ord('q'):
			cap.release()
			cv2.destroyAllWindows()
			exit(0)


	np.savez_compressed(
		save_path,
		objpoints=objpoints,
		imgpoints=imgpoints,
		image_shape=gray.shape[::-1]  # (width, height)
	)
	print(f"[✓] Saved calibration samples to {os.path.abspath(save_path)}")

	cap.release()
	cv2.destroyAllWindows()