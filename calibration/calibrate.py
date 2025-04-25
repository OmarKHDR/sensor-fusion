import numpy as np
import cv2
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from calibration_samples_gen import generate_calibration_samples


def calibrate_from_samples(samples_path="calibration/calibration_samples.npz", output_path="calibration/camera_calibration.npz"):

    data = np.load(samples_path, allow_pickle=True)
    objpoints = data['objpoints']
    imgpoints = data['imgpoints']
    image_shape = tuple(data['image_shape'])  # (width, height)

    print(f"[o] Loaded {len(objpoints)} calibration samples")

    # Calibrate the camera
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, image_shape, None, None
    )

    if not ret:
        print("[x] Calibration failed.")
        return

    print("[o] Calibration successful")
    print("Camera matrix:")
    print(camera_matrix)
    print("Distortion coefficients:")
    print(dist_coeffs)

    # Save the calibration result
    np.savez_compressed(output_path,
                        camera_matrix=camera_matrix,
                        dist_coeffs=dist_coeffs,
                        rvecs=rvecs,
                        tvecs=tvecs)
    print(f"[o] Saved calibration data to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    generate_calibration_samples()
    calibrate_from_samples()
