import os
from core.server_detector import find_server_dir

SERVER_DIR = find_server_dir()

SETTINGS_DIR = (
    os.path.join(SERVER_DIR, "save-data", "Settings")
    if SERVER_DIR else None
)

HOST_FILE = (
    os.path.join(SETTINGS_DIR, "ServerHostSettings.json")
    if SETTINGS_DIR else None
)

GAME_FILE = (
    os.path.join(SETTINGS_DIR, "ServerGameSettings.json")
    if SETTINGS_DIR else None
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FALLBACK_DIR = os.path.join(BASE_DIR, "referencia")

FALLBACK_HOST_FILE = os.path.join(
    FALLBACK_DIR,
    "ServerHostSettings.json"
)

FALLBACK_GAME_FILE = os.path.join(
    FALLBACK_DIR,
    "ServerGameSettings.json"
)