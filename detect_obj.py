#!/usr/bin/env python3
import math
import cv2
from ultralytics import YOLO
import numpy as np
import json
import sys
from pathlib import Path

# Append parent directory to import cap
sys.path.append(str(Path(__file__).parent))
from calibration.trycamera import init_camera

def detector(cap):
    def polar_to_camera_coords(r_cm, theta_deg):
        theta_rad = math.radians(theta_deg)
        x = r_cm * math.sin(theta_rad)   # horizontal offset (X)
        y = 0                            # flat plane (Y)
        z = r_cm * math.cos(theta_rad)   # forward distance (Z)
        return np.array([[x, y, z]], dtype=np.float32)

    def project_to_image(object_point_3D):
        image_points, _ = cv2.projectPoints(object_point_3D, rvec, tvec, camera_matrix, dist_coeffs)
        print(f"3D point {object_point_3D[0]} -> 2D point {image_points[0][0]}")
        print("==================================")
        return tuple(image_points[0][0])

    def point_in_box(point, x1, y1, x2, y2):
        px, py = point
        return x1 <= px <= x2 and y1 <= py <= y2

    try:
        data = np.load("calibration/camera_calibration.npz", allow_pickle=True)
        camera_matrix = data['camera_matrix']
        dist_coeffs = data['dist_coeffs']

        rvec = np.array([[0.0], [0.0], [0.0]], dtype=np.float32)
        tvec = np.array([[0.0], [0.0], [0.0]], dtype=np.float32)

        print("[o] loaded calibration results:")
        print("==================================")
        print("Camera Matrix:\n", camera_matrix)
        print("==================================")
        print("distortion coeffecients:\n", dist_coeffs)
        print("==================================")
    except Exception as e:
        print("[x] coudnt load the caliration data, do calibration again", e)
        return

    # Load ultrasonic data
    try:
        with open(Path(__file__).parent/"ultrasonic.json") as ultra:
            obj = json.load(ultra)
            r, theta = obj["r"], obj["theta"]
            print("[o] loaded radius and theta values:", r, theta)
    except Exception:
        print("[x] couldn't load the radius and the theta — try again later")
        exit(1)

    # Initialize YOLO once
    model = YOLO("yolov8n.pt")

    if not cap:
        print("[x] camera is not working, try again ...")
        return


    object_point = polar_to_camera_coords(r, theta)
    projected_point = project_to_image(object_point)
    px, py = int(projected_point[0]), int(projected_point[1])

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[x] Failed to grab frame")
            continue

        # Draw green circle at projected location
        cv2.circle(frame, (px, py), 8, (0, 255, 0), -1)

        # Run YOLO detection
        results = model(frame, verbose=False)
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                if point_in_box((px, py), x1, y1, x2, y2):
                    # Highlight target object
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 3)
                    cv2.putText(frame, f"Target Object: {model.names[cls]} {conf:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                else:
                    # Normal detected objects
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, f"{model.names[cls]} {conf:.2f}", (x1, y1 - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        # Display
        cv2.imshow("lets do this", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
