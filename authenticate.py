import os
import time
import cv2
import face_recognition
import pickle
import sys
from scipy.spatial import distance as dist

os.chdir("/home/shivam45783/face_unlock")

# ------------------------------
# Load all registered faces (multi-user + multi-sample)
# ------------------------------
known_encodings = []
known_users = []

faces_dir = "faces"

for user in os.listdir(faces_dir):

    user_path = os.path.join(faces_dir,user)

    if not os.path.isdir(user_path):
        continue

    for file in os.listdir(user_path):

        if file.endswith(".pkl"):

            with open(os.path.join(user_path,file),"rb") as f:
                known_encodings.append(pickle.load(f))
                known_users.append(user)

with open("/tmp/face_debug.txt","a") as f:
    f.write("Script started\n")

video = cv2.VideoCapture(2)

frames_to_check = 15
matches = 0

blink_detected = False

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

    if len(frame.shape) == 2:
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)

    if len(face_locations) == 0:
        continue

    encodings = face_recognition.face_encodings(rgb, face_locations)
    landmarks = face_recognition.face_landmarks(rgb)

    if len(encodings) == 0 or len(landmarks) == 0:
        continue

    # ------------------------------
    # Face recognition (multi-user + multi-sample)
    # ------------------------------
    distances = face_recognition.face_distance(known_encodings, encodings[0])

    best_distance = min(distances)
    best_index = distances.tolist().index(best_distance)

    matched_user = known_users[best_index]

    print("Best match:", matched_user)
    print("Face distance:", best_distance)

    if best_distance < 0.5:
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

    if ear < 0.23:
        blink_detected = True

video.release()

print("Matches:", matches)
print("Blink detected:", blink_detected)

# ------------------------------
# Final authentication decision
# ------------------------------
if matches >= 5 and blink_detected:
    print("Authentication successful (live user)")
    sys.exit(0)
else:
    print("Authentication failed")
    sys.exit(1)