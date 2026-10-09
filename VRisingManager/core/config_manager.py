import json
import os

import customtkinter as ctk


class ConfigManager:
    DEFAULT_HOST = {
        "Name": "",
        "Password": "",
        "MaxConnectedUsers": 20,
        "SaveName": "world1",
        "GamePort": 9876,
        "QueryPort": 9877,
        "Worlds": ["world1"],
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
        self.profile_file = os.path.join(self.settings_dir, "profiles.json") if self.settings_dir else None
        self.host = dict(self.DEFAULT_HOST)
        self.game = {}
        self.profiles = {"Default": dict(self.DEFAULT_HOST)}
        self.active_profile = "Default"
        self.load_configs()
        self.load_profiles()

    def merge_worlds(self, *world_groups):
        merged = []
        seen = set()

        for group in world_groups:
            if not group:
                continue
            if isinstance(group, (str, bytes)):
                items = [group]
            else:
                items = list(group)

            for value in items:
                if value is None:
                    continue
                world_name = str(value).strip()
                if not world_name or world_name in seen:
                    continue
                merged.append(world_name)
                seen.add(world_name)

        return merged

    def normalize_world_data(self, data):
        if not isinstance(data, dict):
            data = {}

        discovered = self.discover_worlds()
        save_name = str(data.get("SaveName", "") or "").strip()
        worlds = self.merge_worlds(discovered, data.get("Worlds", []), [save_name])

        if not worlds:
            worlds = ["world1"]

        data["Worlds"] = worlds
        data["SaveName"] = save_name if save_name in worlds else worlds[0]
        return data

    def discover_worlds(self):
        if not self.server_dir:
            return ["world1"]

        save_root = os.path.join(self.server_dir, "save-data")
        if not os.path.isdir(save_root):
            return ["world1"]

        worlds = []
        seen = set()
        reserved_dirs = {"Settings", "Logs", "Backups", "Saves", "v4", "v3", "v2", "v1"}

        for current_root, directories, _ in os.walk(save_root):
            for directory in list(directories):
                if directory in {"Settings", "Logs", "Backups"}:
                    directories.remove(directory)
                    continue

                if directory in {"Saves", "v4", "v3", "v2", "v1"}:
                    continue

                candidate = os.path.join(current_root, directory)
                if os.path.isdir(candidate):
                    world_name = directory.strip()
                    if world_name and world_name not in seen:
                        worlds.append(world_name)
                        seen.add(world_name)

            directories[:] = [
                directory for directory in directories
                if directory not in {"Settings", "Logs", "Backups"}
            ]

        if not worlds:
            worlds = ["world1"]
        return worlds

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

        for key, default_value in self.DEFAULT_HOST.items():
            self.host.setdefault(key, default_value)

        return host_path, game_path

    def load_profiles(self):
        default_profiles = {"Default": dict(self.DEFAULT_HOST)}

        if not self.profile_file:
            self.profiles = default_profiles
            self.active_profile = "Default"
            return self.profiles

        try:
            with open(self.profile_file, "r", encoding="utf-8") as handle:
                loaded = json.load(handle)
            if isinstance(loaded, dict):
                self.profiles = {str(k): dict(v) for k, v in loaded.items() if isinstance(v, dict)}
            else:
                self.profiles = default_profiles
        except Exception:
            self.profiles = default_profiles

        if not self.profiles:
            self.profiles = default_profiles

        for key, value in default_profiles.items():
            self.profiles.setdefault(key, dict(value))

        for profile_name, profile_data in self.profiles.items():
            if not isinstance(profile_data, dict):
                continue
            profile_data = self.normalize_world_data(profile_data)
            self.profiles[profile_name] = profile_data

        self.active_profile = next(iter(self.profiles), "Default")
        return self.profiles

    def save_profiles(self):
        if not self.profile_file:
            return self.profiles

        os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)

        with open(self.profile_file, "w", encoding="utf-8") as handle:
            json.dump(self.profiles, handle, indent=2)

        return self.profiles

    def save_profile(self, profile_name, host_values=None):
        name = (profile_name or "Default").strip() or "Default"
        data = dict(self.DEFAULT_HOST)

        if host_values:
            data.update(host_values)

        data = self.normalize_world_data(data)
        self.profiles[name] = data
        self.active_profile = name
        self.save_profiles()
        return data

    def load_profile(self, profile_name):
        name = profile_name or "Default"
        profile = self.profiles.get(name, dict(self.DEFAULT_HOST))
        self.active_profile = name
        self.host = dict(self.DEFAULT_HOST)
        self.host.update(profile)
        self.host = self.normalize_world_data(self.host)
        return dict(self.host)

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

        profile_name = (host_values or {}).get("ProfileName") or self.active_profile
        self.save_profile(profile_name, self.host)

        target_host = self.host_file or self.fallback_host_file
        target_game = self.game_file or self.fallback_game_file

        os.makedirs(os.path.dirname(target_host), exist_ok=True)
        os.makedirs(os.path.dirname(target_game), exist_ok=True)

        with open(target_host, "w", encoding="utf-8") as handle:
            json.dump(self.host, handle, indent=2)

        with open(target_game, "w", encoding="utf-8") as handle:
            json.dump(self.game, handle, indent=2)

        return target_host, target_game