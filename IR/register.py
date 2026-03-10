import cv2
import face_recognition
import pickle
import os
import sys
import numpy as np

BASE_DIR = "/home/shivam45783/face_unlock"
FACES_DIR = os.path.join(BASE_DIR, "faces")

if len(sys.argv) != 2:
    print("Usage: python register.py <username>")
    sys.exit(1)

username = sys.argv[1]

user_dir = os.path.join(FACES_DIR, username)
os.makedirs(user_dir, exist_ok=True)

# ------------------------------
# IR Camera Index
# ------------------------------
IR_CAMERA_INDEX = 2   # change if needed

video = cv2.VideoCapture(IR_CAMERA_INDEX)

sample_count = 0
MAX_SAMPLES = 10

print("Capturing face samples using IR camera...")

while sample_count < MAX_SAMPLES:

    ret, frame = video.read()

    if not ret:
        continue

    # ------------------------------
    # Handle grayscale IR frames
    # ------------------------------
    if len(frame.shape) == 2:
        frame = cv2.equalizeHist(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    small = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)

    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)

    if len(faces) != 1:
        print("Ensure only one face is visible")
        continue

    encodings = face_recognition.face_encodings(rgb, faces)

    if len(encodings) == 0:
        continue

    encoding = encodings[0]

    file_path = os.path.join(user_dir, f"{sample_count+1}.pkl")

    with open(file_path, "wb") as f:
        pickle.dump(encoding, f)

    sample_count += 1

    print("Saved sample", sample_count)

video.release()

print("Registration completed for", username)