import numpy as np
import cv2
import os

def calibrate_from_samples(samples_path="calibration_samples.npz", output_path="camera_calibration.npz"):
    # Load calibration samples
    data = np.load(samples_path, allow_pickle=True)
    objpoints = data['objpoints']
    imgpoints = data['imgpoints']
    image_shape = tuple(data['image_shape'])  # (width, height)

    print(f"[✓] Loaded {len(objpoints)} calibration samples")

    # Calibrate the camera
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, image_shape, None, None
    )

    if not ret:
        print("[-] Calibration failed.")
        return

    print("[✓] Calibration successful")
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
    print(f"[✓] Saved calibration data to {os.path.abspath(output_path)}")

if __name__ == "__main__":
    calibrate_from_samples()
