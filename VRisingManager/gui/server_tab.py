import customtkinter as ctk

from data.theme import FUNDO, PAINEL, PAINEL_2, VERMELHO, VERMELHO_HOVER


class ServerTab:
    def __init__(self, parent, config_manager, style_entry, on_save):
        self.parent = parent
        self.config_manager = config_manager
        self.style_entry = style_entry
        self.on_save = on_save
        self.build()

    def section_title(self, parent, title):
        header = ctk.CTkFrame(parent, fg_color=PAINEL_2, corner_radius=0)
        header.pack(fill="x", pady=(0, 8))
        ctk.CTkLabel(header, text=title, font=("Segoe UI", 15, "bold"), anchor="w", text_color="#F4F5F7").pack(anchor="w", padx=12, pady=10)
        return header

    def build(self):
        outer = ctk.CTkFrame(self.parent, fg_color=FUNDO)
        outer.pack(fill="both", expand=True, padx=14, pady=14)

        self.available_worlds = self.config_manager.discover_worlds()
        self.profile_name_var = ctk.StringVar(value=self.config_manager.active_profile)

        profile_frame = self.section_title(outer, "Perfil do servidor")
        self.profile_combo = ctk.CTkComboBox(profile_frame, values=list(self.config_manager.profiles.keys()), variable=self.profile_name_var, width=260, corner_radius=0, border_color=VERMELHO)
        self.profile_combo.pack(fill="x", padx=12, pady=(0, 10))

        profile_row = ctk.CTkFrame(profile_frame, fg_color=FUNDO, corner_radius=0)
        profile_row.pack(fill="x", padx=12, pady=(0, 12))

        self.profile_label = ctk.CTkEntry(profile_row)
        self.profile_label.insert(0, self.config_manager.active_profile)
        self.style_entry(self.profile_label)
        self.profile_label.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkButton(profile_row, text="Salvar Perfil", fg_color=VERMELHO, hover_color=VERMELHO_HOVER, command=self.save_profile, width=120, corner_radius=0).pack(side="left", padx=(0, 8))
        ctk.CTkButton(profile_row, text="Carregar", command=self.load_selected_profile, width=90, corner_radius=0).pack(side="left")

        server_frame = self.section_title(outer, "Configuração do host")
        basic_grid = ctk.CTkFrame(server_frame, fg_color=FUNDO, corner_radius=0)
        basic_grid.pack(fill="both", padx=12, pady=(0, 12))

        ctk.CTkLabel(basic_grid, text="Nome do Servidor", text_color="#E8EBF0").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 6))
        self.name = ctk.CTkEntry(basic_grid)
        self.name.insert(0, self.config_manager.host.get("Name", ""))
        self.style_entry(self.name)
        self.name.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(basic_grid, text="Senha", text_color="#E8EBF0").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=(0, 6))
        self.password = ctk.CTkEntry(basic_grid, show="*")
        self.password.insert(0, self.config_manager.host.get("Password", ""))
        self.style_entry(self.password)
        self.password.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(basic_grid, text="Jogadores Máximos", text_color="#E8EBF0").grid(row=2, column=0, sticky="w", padx=(0, 12), pady=(0, 6))
        self.max_users = ctk.CTkEntry(basic_grid)
        self.max_users.insert(0, str(self.config_manager.host.get("MaxConnectedUsers", 20)))
        self.style_entry(self.max_users)
        self.max_users.grid(row=2, column=1, sticky="ew", pady=(0, 6))

        basic_grid.columnconfigure(1, weight=1)

        world_frame = self.section_title(outer, "Mapa / Save")
        self.save_combo = ctk.CTkComboBox(world_frame, values=self.available_worlds, width=260, corner_radius=0, border_color=VERMELHO)
        self.save_combo.set(self.config_manager.host.get("SaveName", self.available_worlds[0]))
        self.save_combo.pack(fill="x", padx=12, pady=(0, 10))

        world_row = ctk.CTkFrame(world_frame, fg_color=FUNDO, corner_radius=0)
        world_row.pack(fill="x", padx=12, pady=(0, 12))
        self.save_name = ctk.CTkEntry(world_row)
        self.save_name.insert(0, self.config_manager.host.get("SaveName", self.available_worlds[0]))
        self.style_entry(self.save_name)
        self.save_name.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(world_row, text="Atualizar Saves", command=self.refresh_worlds, width=120, corner_radius=0).pack(side="left")

        network_frame = self.section_title(outer, "Rede")
        net_grid = ctk.CTkFrame(network_frame, fg_color=FUNDO, corner_radius=0)
        net_grid.pack(fill="both", padx=12, pady=(0, 12))

        ctk.CTkLabel(net_grid, text="Porta do Jogo", text_color="#E8EBF0").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=(0, 6))
        self.game_port = ctk.CTkEntry(net_grid)
        self.game_port.insert(0, str(self.config_manager.host.get("GamePort", 9876)))
        self.style_entry(self.game_port)
        self.game_port.grid(row=0, column=1, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(net_grid, text="Porta de Query", text_color="#E8EBF0").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=(0, 6))
        self.query_port = ctk.CTkEntry(net_grid)
        self.query_port.insert(0, str(self.config_manager.host.get("QueryPort", 9877)))
        self.style_entry(self.query_port)
        self.query_port.grid(row=1, column=1, sticky="ew", pady=(0, 6))

        net_grid.columnconfigure(1, weight=1)

        ctk.CTkButton(
            outer,
            text="Salvar Configurações",
            fg_color=VERMELHO,
            hover_color=VERMELHO_HOVER,
            command=self.on_save,
            height=42,
            width=240,
            corner_radius=0,
        ).pack(pady=(12, 4))

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
