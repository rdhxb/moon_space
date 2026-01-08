# game/data/items.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


# Kategorie pomagają w UI (filtry) i w logice (np. "czy to consumable?")
ITEM_CATEGORIES = {
    "resource",
    "consumable",
    "component",
    "module",
    "quest",
}


@dataclass(frozen=True, slots=True)
class ItemDef:
    id: str
    name: str
    category: str
    stack_max: int

    # Opcjonalne, ale bardzo szybko się przydają
    value: int = 0              # do sprzedaży/ekonomii
    description: str = ""
    icon: str | None = None     # np. ścieżka do ikonki w UI (później)


ITEMS: Dict[str, ItemDef] = {
    # RESOURCES
    "iron_ore": ItemDef(
        id="iron_ore",
        name="Ruda żelaza",
        category="resource",
        stack_max=50,
        value=2,
        description="Podstawowy surowiec do rafinacji i craftingu.",
    ),
    "copper_ore": ItemDef(
        id="copper_ore",
        name="Ruda miedzi",
        category="resource",
        stack_max=50,
        value=3,
        description="Przydatna do elektroniki i przewodników.",
    ),
}

def get_item(item_id: str) -> ItemDef:
    """Zwraca definicję itemu albo rzuca KeyError (celowo – to błąd danych)."""
    return ITEMS[item_id]


def is_stackable(item_id: str) -> bool:
    return get_item(item_id).stack_max > 1


def validate_items() -> None:
    for k, v in ITEMS.items():
        assert k == v.id, f"ITEMS key '{k}' != ItemDef.id '{v.id}'"
        assert v.category in ITEM_CATEGORIES, f"Unknown category: {v.category}"
        assert v.stack_max >= 1, f"Invalid stack_max for {v.id}"