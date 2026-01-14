import pygame
ITEMS = {
    "iron_ore": {
        "name": "Ruda żelaza",
        "category": "resource",
        "stack_max": 50,
        "value": 4,
        "description": "Podstawowy surowiec do rafinacji i craftingu.",
    },

    # --- MARS ORES ---
    "hematite_ore": {
        "name": "Ruda hematytu",
        "category": "resource",
        "stack_max": 50,
        "value": 6,
        "description": "Bogata w żelazo ruda marsjańska. Dobra do rafinacji.",
    },

    "ferrosilicate_ore": {
        "name": "Ruda żelazokrzemianów",
        "category": "resource",
        "stack_max": 50,
        "value": 7,
        "description": "Złoże żelazokrzemianowe. Może wymagać lepszej rafinacji.",
    },

    "sulfide_ore": {
        "name": "Ruda siarczkowa",
        "category": "resource",
        "stack_max": 50,
        "value": 9,
        "description": "Ruda siarczkowa z domieszkami metali. Cenniejsza od podstawowej.",
    },
}

def get_item(item_id: str) -> dict:
    return ITEMS[item_id]

def stack_max(item_id: str) -> int:
    return ITEMS[item_id]["stack_max"]

def validate_items() -> None:
    for item_id, data in ITEMS.items():
        assert "name" in data
        assert "category" in data
        assert "stack_max" in data
        assert data["stack_max"] >= 1
