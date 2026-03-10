import os
import cv2
import face_recognition
import pickle
import sys
import numpy as np
from scipy.spatial import distance as dist

os.chdir("/home/shivam45783/face_unlock")

# ------------------------------
# Load registered faces
# ------------------------------
known_encodings = []
known_users = []

faces_dir = "faces"

for user in os.listdir(faces_dir):

    user_path = os.path.join(faces_dir, user)

    if not os.path.isdir(user_path):
        continue

    for file in os.listdir(user_path):

        if file.endswith(".pkl"):

            with open(os.path.join(user_path, file), "rb") as f:
                known_encodings.append(pickle.load(f))
                known_users.append(user)

# ------------------------------
# Camera
# ------------------------------
video = cv2.VideoCapture(0)

frames_to_check = 25
matches = 0

# ------------------------------
# Blink detection parameters
# ------------------------------
EAR_THRESHOLD = 0.23

blink_detected = False
prev_ear = 1.0


# ------------------------------
# Blink detection function
# ------------------------------
def eye_aspect_ratio(eye):

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    return (A + B) / (2.0 * C)


# ------------------------------
# Authentication loop
# ------------------------------
for i in range(frames_to_check):

    ret, frame = video.read()

    if not ret:
        continue

    # Handle grayscale cameras
    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    # ------------------------------
    # Lighting normalization
    # ------------------------------
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
    frame = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    # Noise reduction
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # Resize for faster processing
    small = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)

    if len(face_locations) == 0:
        continue

    encodings = face_recognition.face_encodings(rgb, face_locations)
    landmarks = face_recognition.face_landmarks(rgb)

    if len(encodings) == 0 or len(landmarks) == 0:
        continue

    # ------------------------------
    # Face recognition
    # ------------------------------
    distances = face_recognition.face_distance(known_encodings, encodings[0])

    best_distance = min(distances)
    best_index = distances.tolist().index(best_distance)

    matched_user = known_users[best_index]

    print("Best match:", matched_user)
    print("Face distance:", best_distance)

    if best_distance < 0.58:
        matches += 1

    # ------------------------------
    # Blink detection
    # ------------------------------
    lm = landmarks[0]

    left_eye = lm["left_eye"]
    right_eye = lm["right_eye"]

    leftEAR = eye_aspect_ratio(left_eye)
    rightEAR = eye_aspect_ratio(right_eye)

    ear = (leftEAR + rightEAR) / 2.0

    print("EAR:", ear)

    # Detect blink (transition from open -> closed)
    if prev_ear > EAR_THRESHOLD and ear < EAR_THRESHOLD:
        blink_detected = True
        print("Blink detected")

    prev_ear = ear

    # ------------------------------
    # Stop early if success
    # ------------------------------
    if matches >= 4 and blink_detected:
        break

video.release()

print("Matches:", matches)
print("Blink detected:", blink_detected)

# ------------------------------
# Final decision
# ------------------------------
if matches >= 4 and blink_detected:
    print("Authentication successful (live user)")
    sys.exit(0)

else:
    print("Authentication failed")
    sys.exit(1)