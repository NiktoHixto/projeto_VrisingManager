import os

import customtkinter as ctk

from data.theme import FUNDO, PAINEL, PAINEL_2, PRETO, VERMELHO, VERMELHO_ESCURO, VERMELHO_HOVER


class ConsoleTab:
    def __init__(self, parent, server_manager, on_start, on_stop, on_copy_steamid):
        self.parent = parent
        self.server_manager = server_manager
        self.on_start = on_start
        self.on_stop = on_stop
        self.on_copy_steamid = on_copy_steamid
        self.build()

    def build(self):
        frame = ctk.CTkFrame(self.parent, fg_color=FUNDO)
        frame.pack(fill="both", expand=True, padx=14, pady=14)

        top = ctk.CTkFrame(frame, fg_color=PAINEL_2)
        top.pack(fill="x", padx=0, pady=(0, 12))

        ctk.CTkButton(top, text="Iniciar Servidor", fg_color=VERMELHO, hover_color=VERMELHO_HOVER, command=self.on_start, width=140, height=34, corner_radius=0).pack(side="left", padx=(12, 8), pady=10)
        ctk.CTkButton(top, text="Parar Servidor", fg_color=VERMELHO_ESCURO, hover_color=VERMELHO, command=self.on_stop, width=140, height=34, corner_radius=0).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(top, text="Copiar SteamID", command=self.on_copy_steamid, width=130, height=34, corner_radius=0).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(top, text="Abrir Logs", command=lambda: os.startfile(os.path.join(self.server_manager.server_dir or os.getcwd(), "logs")), width=110, height=34, corner_radius=0).pack(side="left", padx=8, pady=10)
        ctk.CTkButton(top, text="Abrir Saves", command=lambda: os.startfile(os.path.join(self.server_manager.server_dir or os.getcwd(), "save-data")), width=110, height=34, corner_radius=0).pack(side="left", padx=(8, 12), pady=10)

        self.console = ctk.CTkTextbox(frame, fg_color=PRETO, text_color="#F3F4F6", font=("Segoe UI", 11), corner_radius=0)
        self.console.configure(state="disabled")
        self.console.pack(fill="both", expand=True, padx=0, pady=0)

    def log(self, text):
        self.console.configure(state="normal")
        self.console.insert("end", text)
        self.console.see("end")
        self.console.configure(state="disabled")
