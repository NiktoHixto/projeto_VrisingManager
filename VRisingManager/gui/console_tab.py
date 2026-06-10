import os

import customtkinter as ctk

from data.theme import PRETO, VERMELHO, VERMELHO_ESCURO, VERMELHO_HOVER


class ConsoleTab:
    def __init__(self, parent, server_manager, on_start, on_stop, on_copy_steamid):
        self.parent = parent
        self.server_manager = server_manager
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_copy_steamid = on_copy_steamid
        self.build()

    def build(self):
        frame = ctk.CTkFrame(self.parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        top = ctk.CTkFrame(frame)
        top.pack(fill="x")

        ctk.CTkButton(top, text="Iniciar Servidor", fg_color=VERMELHO, hover_color=VERMELHO_HOVER, command=self.on_start).pack(side="left", padx=5)
        ctk.CTkButton(top, text="Parar Servidor", fg_color=VERMELHO_ESCURO, hover_color=VERMELHO, command=self.on_stop).pack(side="left", padx=5)
        ctk.CTkButton(top, text="Copiar SteamID", command=self.on_copy_steamid).pack(side="left", padx=5)
        ctk.CTkButton(top, text="Abrir Logs", command=lambda: os.startfile(os.path.join(self.server_manager.server_dir or os.getcwd(), "logs"))).pack(side="left", padx=5)
        ctk.CTkButton(top, text="Abrir Saves", command=lambda: os.startfile(os.path.join(self.server_manager.server_dir or os.getcwd(), "save-data"))).pack(side="left", padx=5)

        self.console = ctk.CTkTextbox(frame, fg_color=PRETO, text_color="#FF5555")
        self.console.configure(state="disabled")
        self.console.pack(fill="both", expand=True, padx=10, pady=10)

    def log(self, text):
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")
