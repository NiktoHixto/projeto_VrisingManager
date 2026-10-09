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
        self.available_worlds = self.config_manager.discover_worlds()
        self.profile_name_var = ctk.StringVar(value=self.config_manager.active_profile)
        self.profile_combo = ctk.CTkComboBox(self.parent, values=list(self.config_manager.profiles.keys()), variable=self.profile_name_var)
        self.profile_combo.pack(fill="x", padx=10, pady=(10, 5))

        profile_row = ctk.CTkFrame(self.parent)
        profile_row.pack(fill="x", padx=10, pady=5)

        self.profile_label = ctk.CTkEntry(profile_row)
        self.profile_label.insert(0, self.config_manager.active_profile)
        self.profile_label.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.style_entry(self.profile_label)

        ctk.CTkButton(profile_row, text="Salvar Perfil", fg_color=VERMELHO, hover_color=VERMELHO_HOVER, command=self.save_profile).pack(side="left")
        ctk.CTkButton(profile_row, text="Carregar", command=self.load_selected_profile).pack(side="left", padx=(5, 0))

        ctk.CTkLabel(self.parent, text="Nome do Servidor").pack(anchor="w", padx=10)
        self.name = ctk.CTkEntry(self.parent)
        self.name.insert(0, self.config_manager.host.get("Name", ""))
        self.style_entry(self.name)
        self.name.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.parent, text="Mapa / Save disponível").pack(anchor="w", padx=10)
        self.save_combo = ctk.CTkComboBox(self.parent, values=self.available_worlds, width=250)
        self.save_combo.set(self.config_manager.host.get("SaveName", self.available_worlds[0]))
        self.save_combo.pack(fill="x", padx=10, pady=5)

        world_row = ctk.CTkFrame(self.parent)
        world_row.pack(fill="x", padx=10, pady=5)
        self.save_name = ctk.CTkEntry(world_row)
        self.save_name.insert(0, self.config_manager.host.get("SaveName", self.available_worlds[0]))
        self.style_entry(self.save_name)
        self.save_name.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ctk.CTkButton(world_row, text="Atualizar Saves", command=self.refresh_worlds).pack(side="left")

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

        ctk.CTkLabel(self.parent, text="Porta do Jogo").pack(anchor="w", padx=10)
        self.game_port = ctk.CTkEntry(self.parent)
        self.game_port.insert(0, str(self.config_manager.host.get("GamePort", 9876)))
        self.style_entry(self.game_port)
        self.game_port.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(self.parent, text="Porta de Query").pack(anchor="w", padx=10)
        self.query_port = ctk.CTkEntry(self.parent)
        self.query_port.insert(0, str(self.config_manager.host.get("QueryPort", 9877)))
        self.style_entry(self.query_port)
        self.query_port.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            self.parent,
            text="Salvar Configurações",
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            command=self.on_save,
        ).pack(pady=10)

    def refresh_worlds(self):
        current_value = self.save_name.get().strip() or self.save_combo.get().strip()
        self.available_worlds = self.config_manager.merge_worlds(
            self.config_manager.discover_worlds(),
            [current_value] if current_value else [],
        )
        self.save_combo.configure(values=self.available_worlds)
        if self.available_worlds:
            selected = current_value if current_value in self.available_worlds else self.available_worlds[0]
            self.save_combo.set(selected)
            self.save_name.delete(0, "end")
            self.save_name.insert(0, selected)

    def save_profile(self):
        profile_name = self.profile_label.get().strip() or self.profile_name_var.get()
        profile_data = self.collect()
        profile_data["ProfileName"] = profile_name
        self.config_manager.save_profile(profile_name, profile_data)
        self.profile_name_var.set(profile_name)
        self.profile_combo.configure(values=list(self.config_manager.profiles.keys()))
        self.profile_combo.set(profile_name)

    def load_selected_profile(self):
        profile_name = self.profile_name_var.get() or self.profile_label.get() or "Default"
        if profile_name not in self.config_manager.profiles:
            return

        profile = self.config_manager.load_profile(profile_name)
        self.profile_label.delete(0, "end")
        self.profile_label.insert(0, profile_name)
        self.name.delete(0, "end")
        self.name.insert(0, profile.get("Name", ""))
        selected_save = profile.get("SaveName") or (profile.get("Worlds", ["world1"])[0] if profile.get("Worlds") else "world1")
        self.save_name.delete(0, "end")
        self.save_name.insert(0, selected_save)
        self.save_combo.set(selected_save)
        self.password.delete(0, "end")
        self.password.insert(0, profile.get("Password", ""))
        self.max_users.delete(0, "end")
        self.max_users.insert(0, str(profile.get("MaxConnectedUsers", 20)))
        self.game_port.delete(0, "end")
        self.game_port.insert(0, str(profile.get("GamePort", 9876)))
        self.query_port.delete(0, "end")
        self.query_port.insert(0, str(profile.get("QueryPort", 9877)))

    def collect(self):
        save_name = (self.save_name.get() or self.save_combo.get() or "world1").strip()
        if save_name:
            self.save_name.delete(0, "end")
            self.save_name.insert(0, save_name)
            self.save_combo.set(save_name)

        discovered = self.config_manager.discover_worlds()
        worlds = self.config_manager.merge_worlds(discovered, [save_name], self.config_manager.profiles.get(self.profile_name_var.get(), {}).get("Worlds", []))
        if not worlds:
            worlds = [save_name or "world1"]

        self.save_combo.configure(values=worlds)
        self.save_combo.set(save_name if save_name in worlds else worlds[0])

        return {
            "ProfileName": self.profile_label.get().strip() or self.profile_name_var.get() or "Default",
            "Name": self.name.get(),
            "SaveName": save_name or "world1",
            "Password": self.password.get(),
            "MaxConnectedUsers": int(self.max_users.get() or 20),
            "GamePort": int(self.game_port.get() or 9876),
            "QueryPort": int(self.query_port.get() or 9877),
            "Worlds": worlds,
        }
