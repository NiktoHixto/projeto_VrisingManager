import os

import customtkinter as ctk

from core.config_manager import ConfigManager
from core.paths import FALLBACK_GAME_FILE, FALLBACK_HOST_FILE, GAME_FILE, HOST_FILE, SERVER_DIR, SETTINGS_DIR
from core.server_manager import ServerManager
from data.theme import VERMELHO, VERMELHO_HOVER
from gui.console_tab import ConsoleTab
from gui.gameplay_tab import GameplayTab
from gui.server_tab import ServerTab


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "vrising.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass

        self.title("V Rising Manager")
        self.geometry("1100x750")

        ctk.set_appearance_mode("dark")

        self.config_manager = ConfigManager(
            server_dir=SERVER_DIR,
            settings_dir=SETTINGS_DIR,
            host_file=HOST_FILE,
            game_file=GAME_FILE,
            fallback_host_file=FALLBACK_HOST_FILE,
            fallback_game_file=FALLBACK_GAME_FILE,
        )

        self.server_manager = ServerManager(SERVER_DIR)
        self.steamid = ""

        self.status_var = ctk.StringVar(value="Status: Offline")
        self.status_label = ctk.CTkLabel(self, textvariable=self.status_var, font=("Segoe UI", 18, "bold"), text_color="#FF4444")
        self.status_label.pack(pady=5)

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_server = self.tabs.add("Servidor")
        self.tab_game = self.tabs.add("Gameplay")
        self.tab_console = self.tabs.add("Console")

        self.server_tab = ServerTab(self.tab_server, self.config_manager, self.style_entry, self.save_all)
        self.gameplay_tab = GameplayTab(self.tab_game, self.config_manager.game)
        self.console_tab = ConsoleTab(self.tab_console, self.server_manager, self.start_server, self.stop_server, self.copy_steamid)

        if not SERVER_DIR:
            self.set_status("Status: Servidor não encontrado. Use a pasta correta.", "#FF4444")
        else:
            self.set_status(f"Status: Diretório do servidor detectado: {SERVER_DIR}", "#FFD700")

    def style_entry(self, entry):
        entry.configure(fg_color="#1A1A1A", border_color="#8B0000")

    def set_status(self, text, color):
        self.status_var.set(text)
        self.status_label.configure(text_color=color)

    def save_all(self):
        host_values = self.server_tab.collect()
        self.config_manager.save_all(host_values, self.gameplay_tab.game_widgets)
        self.console_tab.log(f"Configurações salvas em {os.path.dirname(self.config_manager.host_file or self.config_manager.fallback_host_file)}.\n")

    def copy_steamid(self):
        if not self.server_manager.steamid:
            self.console_tab.log("SteamID ainda não detectado.\n")
            return

        self.clipboard_clear()
        self.clipboard_append(self.server_manager.steamid)
        self.console_tab.log(f"SteamID copiado: {self.server_manager.steamid}\n")

    def start_server(self):
        if self.server_manager.proc:
            return

        try:
            self.server_manager.start(self.server_tab.name.get(), on_line=self.console_tab.log, on_status=self.set_status)
        except Exception as exc:
            self.console_tab.log(f"Erro ao iniciar servidor: {exc}\n")
            self.set_status("Status: Falha ao iniciar servidor", "#FF4444")
            return

        self.set_status("Status: Iniciando...", "#FFD700")
        self.console_tab.log("Servidor iniciado.\n")

    def stop_server(self):
        if self.server_manager.stop():
            self.set_status("Status: Offline", "#FF4444")
            self.console_tab.log("Servidor parado.\n")
