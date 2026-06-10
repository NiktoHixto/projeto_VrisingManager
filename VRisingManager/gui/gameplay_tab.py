import json

import customtkinter as ctk

from data.theme import PRETO2, VERMELHO
from data.tooltips import TOOLTIPS
from data.translations import prettify_name


class GameplayTab:
    def __init__(self, parent, game_data):
        self.parent = parent
        self.game = game_data
        self.game_widgets = {}
        self.build()

    def build(self):
        scroll = ctk.CTkScrollableFrame(self.parent)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        self.frame = scroll
        self.create_json_widgets(self.frame, self.game, "")

    def create_json_widgets(self, parent, data, path):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key

            if isinstance(value, dict):
                frame = ctk.CTkFrame(parent)
                frame.pack(fill="x", padx=5, pady=5)

                header = ctk.CTkFrame(frame)
                header.pack(fill="x")

                label = ctk.CTkLabel(header, text=f"▼ {prettify_name(key)}", font=("Segoe UI", 14, "bold"))
                label.pack(side="left", padx=5, pady=5)

                info = ctk.CTkLabel(header, text="ⓘ", text_color="#00AEEF")
                info.pack(side="left", padx=5)
                from gui.tooltip import ToolTip

                ToolTip(info, TOOLTIPS.get(key, f"Grupo de configurações: {key}"))
                self.create_json_widgets(frame, value, current_path)
                continue

            if isinstance(value, bool):
                var = ctk.BooleanVar(value=value)
                frame = ctk.CTkFrame(parent)
                frame.pack(fill="x", padx=10, pady=2)
                chk = ctk.CTkCheckBox(frame, text=prettify_name(key), variable=var)
                chk.pack(side="left")
                info = ctk.CTkLabel(frame, text="ⓘ", text_color="#00AEEF")
                info.pack(side="left", padx=5)
                from gui.tooltip import ToolTip

                ToolTip(info, TOOLTIPS.get(key, "Sem descrição disponível."))
                self.game_widgets[current_path] = var
                continue

            if isinstance(value, (int, float, str)):
                frame = ctk.CTkFrame(parent)
                frame.pack(fill="x")
                label = ctk.CTkLabel(frame, text=prettify_name(key))
                label.pack(side="left")
                info = ctk.CTkLabel(frame, text="ⓘ", text_color="#00AEEF")
                info.pack(side="left", padx=5)
                from gui.tooltip import ToolTip

                ToolTip(info, TOOLTIPS.get(key, "Sem descrição disponível."))
                entry = ctk.CTkEntry(frame, height=32)
                entry.insert(0, str(value))
                entry.pack(fill="x", padx=10, pady=2)
                entry.configure(fg_color=PRETO2, border_color=VERMELHO)
                self.game_widgets[current_path] = entry
                continue

            frame = ctk.CTkFrame(parent)
            frame.pack(fill="x", padx=10, pady=5)
            txt = ctk.CTkTextbox(frame, height=80)
            txt.insert("1.0", json.dumps(value, indent=2))
            txt.pack(fill="x", padx=10, pady=5)
            self.game_widgets[current_path] = txt
