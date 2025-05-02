import numpy as np
import cv2
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from calibration.calibration_samples_gen import generate_calibration_samples


def calibrate_from_samples(samples_path="calibration/calibration_samples.npz", output_path="calibration/camera_calibration.npz"):

    try:
        print("trying to load samples.....")
        data = np.load(samples_path, allow_pickle=True)
        objpoints = data['objpoints']
        imgpoints = data['imgpoints']
        image_shape = tuple(data['image_shape'])  # (width, height)
    except Exception as e:
        print("[x] couldn't load samples, try calibration again", e)
        print("==================================")
        return
    print(f"[o] Loaded {len(objpoints)} calibration samples successfully!")
    print("==================================")

    # Calibrate the camera
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, image_shape, None, None
    )

    if not ret:
        print("[x] Calibration failed. for some reason")
        print("==================================")
        return

    print("[o] Calibration successful")
    print("==================================")
    print("Camera matrix:")
    print(camera_matrix)
    print("==================================")
    print("Distortion coefficients:")
    print(dist_coeffs)
    print("==================================")

    # Save the calibration result
    np.savez_compressed(output_path,
                        camera_matrix=camera_matrix,
                        dist_coeffs=dist_coeffs,
                        rvecs=rvecs,
                        tvecs=tvecs)
    print(f"[o] Saved calibration data to {os.path.abspath(output_path)}")
    print("==================================")

if __name__ == "__main__":
    generate_calibration_samples()
    calibrate_from_samples()
