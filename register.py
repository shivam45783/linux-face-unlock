import cv2
import face_recognition
import pickle
import os
import sys

BASE_DIR = "/home/shivam45783/face_unlock"
FACES_DIR = os.path.join(BASE_DIR, "faces")

if len(sys.argv) != 2:
    print("Usage: python register.py <username>")
    sys.exit(1)

username = sys.argv[1]

user_dir = os.path.join(FACES_DIR, username)
os.makedirs(user_dir, exist_ok=True)

video = cv2.VideoCapture(2)

sample_count = 0
MAX_SAMPLES = 10

print("Capturing face samples...")

while sample_count < MAX_SAMPLES:

    ret, frame = video.read()
    if not ret:
        continue

    small = cv2.resize(frame,(0,0),fx=0.25,fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb)

    if len(faces) != 1:
        continue

    encodings = face_recognition.face_encodings(rgb, faces)

    if len(encodings) == 0:
        continue

    encoding = encodings[0]

    file_path = os.path.join(user_dir,f"{sample_count+1}.pkl")

    with open(file_path,"wb") as f:
        pickle.dump(encoding,f)

    sample_count += 1

    print("Saved sample",sample_count)

video.release()

print("Registration completed for",username)