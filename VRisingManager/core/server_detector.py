import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def find_server_dir():
    candidates = [
        os.path.join(BASE_DIR, "referencia"),
        os.path.join(BASE_DIR, "VRisingDedicatedServer"),
        os.path.join(BASE_DIR, "Servidor"),
        os.path.join(BASE_DIR, "Server"),
        r"C:\Program Files (x86)\Steam\steamapps\common\VRisingDedicatedServer",
        r"C:\Program Files\Steam\steamapps\common\VRisingDedicatedServer",
    ]

    for candidate in candidates:
        if os.path.isfile(os.path.join(candidate, "VRisingServer.exe")):
            return candidate

    for root, _, files in os.walk(BASE_DIR):
        if "VRisingServer.exe" in files:
            return root

    return None