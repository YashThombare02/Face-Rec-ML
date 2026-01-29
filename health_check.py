import os

APP_PATH = "C:/face_recognition/app"

if os.path.exists(APP_PATH):
    print(" Application directory exists")
else:
    print(" Application directory missing")
    exit(1)

print(" Health check passed")
