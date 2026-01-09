import pygame
ITEMS = {
    "iron_ore": {
        "name": "Ruda żelaza",
        "category": "resource",
        "stack_max": 50,
        "value": 2,
        "description": "Podstawowy surowiec do rafinacji i craftingu.",
    },
    "copper_ore": {
        "name": "Ruda miedzi",
        "category": "resource",
        "stack_max": 50,
        "value": 3,
        "description": "Przydatna do elektroniki i przewodników.",
        "icon": "game/data/assets/copper_ore.png",
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
