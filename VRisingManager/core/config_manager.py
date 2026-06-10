import json
import os

import customtkinter as ctk


class ConfigManager:
    DEFAULT_HOST = {
        "Name": "",
        "Password": "",
        "MaxConnectedUsers": 20,
    }

    def __init__(
        self,
        server_dir=None,
        settings_dir=None,
        host_file=None,
        game_file=None,
        fallback_host_file=None,
        fallback_game_file=None,
    ):
        self.server_dir = server_dir
        self.settings_dir = settings_dir
        self.host_file = host_file
        self.game_file = game_file
        self.fallback_host_file = fallback_host_file
        self.fallback_game_file = fallback_game_file
        self.host = dict(self.DEFAULT_HOST)
        self.game = {}
        self.load_configs()

    def load_configs(self):
        if self.server_dir and self.settings_dir:
            try:
                os.makedirs(self.settings_dir, exist_ok=True)
            except OSError:
                pass

        host_path = self.host_file if self.host_file and os.path.isfile(self.host_file) else self.fallback_host_file
        game_path = self.game_file if self.game_file and os.path.isfile(self.game_file) else self.fallback_game_file

        try:
            with open(host_path, "r", encoding="utf-8") as handle:
                self.host = json.load(handle)
        except Exception:
            self.host = dict(self.DEFAULT_HOST)

        try:
            with open(game_path, "r", encoding="utf-8") as handle:
                self.game = json.load(handle)
        except Exception:
            self.game = {}

        return host_path, game_path

    def save_game_settings(self, game_widgets):
        for path, widget in game_widgets.items():
            keys = path.split(".")
            target = self.game

            for key in keys[:-1]:
                if key not in target or not isinstance(target[key], dict):
                    target[key] = {}
                target = target[key]

            final_key = keys[-1]

            if isinstance(widget, ctk.BooleanVar):
                target[final_key] = widget.get()
                continue

            if hasattr(widget, "get"):
                value = widget.get()
                original = target.get(final_key)

                if isinstance(original, bool):
                    target[final_key] = value.lower() in ("true", "1", "yes") if isinstance(value, str) else bool(value)
                elif isinstance(original, int):
                    target[final_key] = int(value)
                elif isinstance(original, float):
                    target[final_key] = float(value)
                elif isinstance(original, list):
                    try:
                        target[final_key] = json.loads(value)
                    except Exception:
                        target[final_key] = value
                else:
                    target[final_key] = value

        return self.game

    def save_all(self, host_values=None, game_widgets=None):
        if host_values:
            self.host.update(host_values)

        if game_widgets:
            self.save_game_settings(game_widgets)

        target_host = self.host_file or self.fallback_host_file
        target_game = self.game_file or self.fallback_game_file

        os.makedirs(os.path.dirname(target_host), exist_ok=True)
        os.makedirs(os.path.dirname(target_game), exist_ok=True)

        with open(target_host, "w", encoding="utf-8") as handle:
            json.dump(self.host, handle, indent=2)

        with open(target_game, "w", encoding="utf-8") as handle:
            json.dump(self.game, handle, indent=2)

        return target_host, target_game