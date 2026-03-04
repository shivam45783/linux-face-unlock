# Linux Face Unlock (IR Camera + Liveness Detection)

A custom **face recognition login system for Linux (Ubuntu)** built using Python, OpenCV, and PAM.

Features:

- Face recognition login
- IR camera support
- Multi-user support
- Multiple samples per user
- Blink detection (liveness detection)
- PAM integration
- Works with GNOME login screen

---

# Features

- Passwordless login using face recognition
- Liveness detection via blink detection
- Multiple users supported
- Multiple face samples per user
- Works with Linux PAM authentication
- Compatible with GNOME login manager

---

# Requirements

Ubuntu / Debian based system.

Hardware:

- Webcam or IR camera

Software dependencies:

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
Make the shell file executable

```bash
chmod +x install.sh
```


Run the installer

```bash
./install.sh
```

Activate the environment

```bash
source venv/bin/activate
```

---

# Register Your Face

Create face samples for your user:

```bash
python register.py <username>
```

Example:

```bash
python register.py shivam
```

This will capture multiple samples of your face.

---

# Directory Structure After Registration

```
faces/
  shivam/
    1.pkl
    2.pkl
    3.pkl
```

Each file contains a face embedding.

---

# Test Authentication

Run the authentication script:

```bash
python authenticate.py
```

If your face is detected and blink verification passes, authentication succeeds.

---

# Enable Login Screen Face Unlock

Edit PAM configuration:

```bash
sudo nano /etc/pam.d/gdm-password
```

Add this line before `@include common-auth`:

```
auth sufficient pam_exec.so seteuid /path/to/venv/bin/python /path/to/authenticate.py
```

Example:

```
auth sufficient pam_exec.so seteuid /home/user/linux-face-unlock/venv/bin/python /home/user/linux-face-unlock/authenticate.py
```

Save and reboot.

---


# Remove Keyring Password Popup (Optional)

When logging in with face unlock, the keyring password popup may appear after authentication. This popup appears because the system needs the user's login password to decrypt the stored secrets in the **GNOME Keyring** (such as Wi-Fi passwords, SSH keys, browser credentials, and application tokens). Since face authentication does not provide the login password, the keyring remains locked and asks for the password.

To disable this popup (which can be annoying), you can set the keyring password to **empty**.

## Step 1: Install Seahorse

Install **Seahorse**, the GNOME keyring manager:

```bash
sudo apt install seahorse
```
---
## Step 2: Open the Password Manager

Launch the application by searching for Passwords and Keys in the application menu.

Or start it from terminal:

```bash
seahorse
```
---

## Step 3: Locate the Login Keyring

In the Seahorse window:

1. Look at the left panel.

2. Click on Passwords.

3. You will see a keyring called Login.

The Login keyring is the default keyring that stores most system credentials.

---

## Step 4: Change the Keyring Password

1. Right-click on **Login**.
2. Select Change **Password**.

A dialog will appear asking for:

* **Current password**

* **New password**

* **Confirm password**

Enter your current system password in the Current password field.

---

## Step 5: Set the Password to Empty

Leave the **New password** and **Confirm password** fields completely blank.

Click **Continue**.

GNOME will display a warning saying that storing secrets without encryption is less secure. Accept the warning to continue.

---
## Step 6: Log Out and Log Back In

After changing the keyring password:

1. Log out of your session.

2. Log back in using face unlock.

The keyring popup should no longer appear.
# Security Notes

This system includes:

- face recognition
- blink liveness detection
- multiple frame verification

However it is not a replacement for enterprise biometric systems. It is just a project for fun.


---

# Future Improvements

Possible improvements:

- head pose detection
- anti-photo spoofing
- background recognition daemon
- GPU acceleration
- Wayland support

---

# License

MIT License

---

# Author

Shivam Rajan