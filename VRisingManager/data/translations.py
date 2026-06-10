import re

TRANSLATIONS = {
    "GameModeType": "Modo de Jogo",
    "CastleLimit": "Limite de Castelos",
    "FloorLimit": "Limite de Andares",
    "ServantLimit": "Limite de Servos",
    "ClanSize": "Tamanho Máximo do Clã",
    "TeleportBoundItems": "Teleportar com Itens Vinculados",
    "InventoryStacksModifier": "Multiplicador de Pilhas",
    "MaterialYieldModifier_Global": "Multiplicador de Recursos",
    "DropTableModifier_General": "Multiplicador de Loot",
    "CraftRateModifier": "Velocidade de Fabricação",
    "RefinementRateModifier": "Velocidade de Refinamento",
    "RefinementCostModifier": "Custo de Refinamento",
    "ResearchCostModifier": "Custo de Pesquisa",
    "BuildCostModifier": "Custo de Construção",
    "BloodDrainModifier": "Consumo de Sangue",
    "DurabilityDrainModifier": "Desgaste de Equipamentos",
    "GarlicAreaStrengthModifier": "Efeito do Alho",
    "HolyAreaStrengthModifier": "Efeito da Luz Sagrada",
    "SilverStrengthModifier": "Efeito da Prata",
    "SunDamageModifier": "Dano Solar",
    "DeathDurabilityFactorLoss": "Perda de Durabilidade na Morte",
    "DeathContainerPermission": "Permissão de Saque",
    "PvPProtectionMode": "Proteção PvP",
    "CastleDamageMode": "Modo de Dano ao Castelo",
    "CastleHeartDamageMode": "Dano ao Coração do Castelo",
    "CanLootEnemyContainers": "Saquear Baús Inimigos",
    "CanDestroyEnemyStructures": "Destruir Estruturas Inimigas",
    "PlayerDamageMode": "Modo de Dano entre Jogadores",
    "DayDurationInSeconds": "Duração do Dia",
    "DayStartHour": "Hora Inicial do Dia",
    "VSPlayerWeekdayTime": "Horário PvP (Semana)",
    "VSPlayerWeekendTime": "Horário PvP (Fim de Semana)",
}


def prettify_name(name):
    if name in TRANSLATIONS:
        return TRANSLATIONS[name]

    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = name.replace("_", " ")
    return " ".join(name.split())
