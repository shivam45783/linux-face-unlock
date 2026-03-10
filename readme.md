# Linux Face Unlock (RGB + IR Camera + Liveness Detection)

A custom **face recognition login system for Linux (Ubuntu)** built using **Python, OpenCV, and PAM**.

This project supports **two camera modes**:

- RGB camera
- Infrared (IR) camera

The IR version provides **better reliability in low light and stronger anti-spoof protection**.

---

# Features

- Passwordless login using face recognition
- IR camera support
- RGB camera support
- Multi-user support
- Multiple samples per user
- Blink detection (liveness detection)
- IR texture based anti-spoof detection
- PAM integration
- Works with GNOME login screen

---

# Requirements

Ubuntu / Debian based system.

## Hardware

- Webcam (RGB) **or**
- Infrared (IR) camera

## Software

- Python 3.10+
- OpenCV
- face_recognition
- dlib
- numpy
- scipy

---

# Installation

Clone the repository

```bash
git clone https://github.com/shivam45783/linux-face-unlock.git
cd linux-face-unlock
```

Make the installer executable

```bash
chmod +x install.sh
```

Run the installer

```bash
./install.sh
```

Activate the virtual environment

```bash
source venv/bin/activate
```

---

# Project Structure

```
linux-face-unlock/

RGB/
    register.py
    authenticate.py

IR/
    register.py
    authenticate.py

faces/
    <username>/
        1.pkl
        2.pkl
        3.pkl
```

### RGB folder
Uses the **standard laptop webcam**.

### IR folder
Uses an **infrared camera with additional anti-spoof detection**.

---

# How to Detect if Your Laptop Has an IR Camera

Run:

```bash
lsusb
```

Look for devices such as:

```
IR Camera
Integrated IR Camera
Intel RealSense
```

Another reliable method:

```bash
v4l2-ctl --list-devices
```

Example output:

```
Integrated Camera:
    /dev/video0

Integrated IR Camera:
    /dev/video2
```

Here:

```
video0 → RGB camera
video2 → IR camera
```

Install the tool if it is not installed:

```bash
sudo apt install v4l-utils
```

---

# How to Test the IR Camera

You can preview the camera using:

```bash
ffplay /dev/video2
```

or

```bash
cheese
```

If it is an IR camera, the video will appear:

- black and white
- visible even in very low light

---

# Finding the Camera Index

OpenCV uses camera indexes like:

```
0
1
2
3
```

To detect available cameras run this test script:

```python
import cv2

for i in range(6):
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()

    if ret:
        print("Camera found at index:", i)

    cap.release()
```

Example output:

```
Camera found at index: 0
Camera found at index: 2
```

Usually:

```
0 → RGB camera
2 → IR camera
```

---

# Configure Camera Index in the Code

Inside the **IR scripts**, you will see:

```python
IR_CAMERA_INDEX = 2
```

Change this value if your IR camera uses a different index.

Example:

```python
IR_CAMERA_INDEX = 3
```

---

# Register Your Face

## Using RGB Camera

```bash
cd RGB
python register.py <username>
```

Example:

```bash
python register.py shivam
```

---

## Using IR Camera

```bash
cd IR
python register.py <username>
```

Example:

```bash
python register.py shivam
```

This will capture **10 face samples**.

---

# Directory Structure After Registration

```
faces/
  shivam/
    1.pkl
    2.pkl
    3.pkl
```

Each file contains a **face embedding vector**.

---

# Test Authentication

## RGB Version

```bash
cd RGB
python authenticate.py
```

---

## IR Version

```bash
cd IR
python authenticate.py
```

The IR version performs:

- face recognition
- blink detection
- IR texture anti-spoof detection

Authentication succeeds when:

```
face match
+ blink detected
+ valid IR texture
```

---

# Enable Login Screen Face Unlock

Edit PAM configuration:

```bash
sudo nano /etc/pam.d/gdm-password
```

Add this line before `@include common-auth`:

```
auth sufficient pam_exec.so seteuid /path/to/python /path/to/authenticate.py
```

Example:

```
auth sufficient pam_exec.so seteuid /home/user/linux-face-unlock/venv/bin/python /home/user/linux-face-unlock/IR/authenticate.py
```

Using the **IR version is recommended**.

Save the file and reboot.

---

# Remove Keyring Password Popup (Optional)

When logging in with face unlock, the keyring password popup may appear because the login password is not entered.

To disable this popup, set the **GNOME keyring password to empty**.

## Install Seahorse

```bash
sudo apt install seahorse
```

Launch it:

```bash
seahorse
```

Then go to:

```
Passwords → Login → Change Password
```

Leave the new password **empty**.

Log out and log back in.

---

# Security Notes

This system includes:

- face recognition
- blink liveness detection
- IR texture anti-spoof detection
- multi-frame verification

However it is **not a replacement for enterprise biometric systems**.

It is intended as an **experimental Linux face unlock project**.

---

# Future Improvements

Possible improvements:
- Improve accuracy
- Robust in all lighting conditions
- 3D face depth detection
- head pose liveness detection
- background recognition daemon
- GPU acceleration
- Wayland support

---

# License

MIT License

---

# Author

Shivam Rajan