import customtkinter as ctk

from data.theme import PRETO2, VERMELHO, VERMELHO_HOVER


class ServerTab:
    def __init__(self, parent, config_manager, style_entry, on_save):
        self.parent = parent
        self.config_manager = config_manager
        self.style_entry = style_entry
        self.on_save = on_save
        self.build()

    def build(self):
        ctk.CTkLabel(self.parent, text="Nome do Servidor").pack(anchor="w", padx=10)

        self.name = ctk.CTkEntry(self.parent)
        self.name.insert(0, self.config_manager.host.get("Name", ""))
        self.style_entry(self.name)
        self.name.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.parent, text="Senha").pack(anchor="w", padx=10)

        self.password = ctk.CTkEntry(self.parent, show="*")
        self.password.insert(0, self.config_manager.host.get("Password", ""))
        self.style_entry(self.password)
        self.password.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.parent, text="Jogadores Máximos").pack(anchor="w", padx=10)

        self.max_users = ctk.CTkEntry(self.parent)
        self.max_users.insert(0, str(self.config_manager.host.get("MaxConnectedUsers", 20)))
        self.style_entry(self.max_users)
        self.max_users.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.parent,
            text="Salvar Configurações",
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            command=self.on_save,
        ).pack(pady=10)

    def collect(self):
        return {
            "Name": self.name.get(),
            "Password": self.password.get(),
            "MaxConnectedUsers": int(self.max_users.get()),
        }
