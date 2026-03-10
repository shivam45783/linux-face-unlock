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
# IR Camera
# ------------------------------
IR_CAMERA_INDEX = 2
video = cv2.VideoCapture(IR_CAMERA_INDEX)
video.set(cv2.CAP_PROP_BUFFERSIZE, 1)
frames_to_check = 25
matches = 0

# ------------------------------
# Blink detection
# ------------------------------
EAR_THRESHOLD = 0.23
prev_ear = 1.0
blink_detected = False

# ------------------------------
# Texture anti-spoof
# ------------------------------
texture_valid_frames = 0
TEXTURE_THRESHOLD = 60


def eye_aspect_ratio(eye):

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    return (A + B) / (2.0 * C)


def ir_texture_score(face_roi):

    gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

    # Remove sensor noise
    gray = cv2.GaussianBlur(gray, (3,3), 0)

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    return laplacian.var()


# ------------------------------
# Authentication loop
# ------------------------------
for i in range(frames_to_check):

    ret, frame = video.read()

    if not ret:
        continue

    # Handle grayscale IR frames
    if len(frame.shape) == 2:
        frame = cv2.equalizeHist(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    # Lighting normalization
    ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
    ycrcb[:,:,0] = cv2.equalizeHist(ycrcb[:,:,0])
    frame = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    frame = cv2.GaussianBlur(frame,(5,5),0)

    small = cv2.resize(frame,(0,0),fx=0.5,fy=0.5)

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

    if prev_ear > EAR_THRESHOLD and ear < EAR_THRESHOLD:
        blink_detected = True
        print("Blink detected")

    prev_ear = ear

    # ------------------------------
    # Texture anti-spoof (FACE ROI)
    # ------------------------------
    top, right, bottom, left = face_locations[0]

    face_roi = small[top:bottom, left:right]

    if face_roi.size != 0:

        texture_score = ir_texture_score(face_roi)

        print("Texture score:", texture_score)

        if texture_score > TEXTURE_THRESHOLD:
            texture_valid_frames += 1

    # Early exit
    if matches >= 4 and blink_detected and texture_valid_frames >= 3:
        break


video.release()

print("Matches:", matches)
print("Blink detected:", blink_detected)
print("Texture frames:", texture_valid_frames)

# ------------------------------
# Final decision
# ------------------------------
if matches >= 4 and blink_detected and texture_valid_frames >= 3:

    print("Authentication successful (live user)")
    sys.exit(0)

else:

    print("Authentication failed")
    sys.exit(1)