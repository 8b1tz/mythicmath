APP_AVATAR_PREFIX = "app-avatar:"

AVATAR_PRESET_IDS = {
    "angelic_paladin",
    "dragon",
    "dwarf",
    "elf",
    "mage",
    "mermaid",
    "necromancer",
    "phoenix",
    "vampire",
}


def is_valid_avatar_preset(avatar_id: str) -> bool:
    return avatar_id in AVATAR_PRESET_IDS


def build_avatar_preset_value(avatar_id: str) -> str:
    return f"{APP_AVATAR_PREFIX}{avatar_id}"
