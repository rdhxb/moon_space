
MISSIONS = {
    # 1) Zbierz iron ore (5)
    "m_collect_iron_5": {
        "title": "Pierwsza ruda",
        "desc": "Zbierz rudę żelaza.",
        "type": "collect_item",
        "target": 5,
        "params": {"item_id": "iron_ore"},
        'is_compleated': False
    },

    # 2) Zbierz iron ore (30)
    "m_collect_iron_30": {
        "title": "Zapas na start",
        "desc": "Zbierz 30 rud żelaza.",
        "type": "collect_item",
        "target": 30,
        "params": {"item_id": "iron_ore"},
        'is_compleated': False

    },

    # 3) Otwórz magazyn (1)
    "m_open_storage": {
        "title": "Pierwsza wizyta w magazynie",
        "desc": "Otwórz okno magazynu w bazie.",
        "type": "open_ui",
        "target": 1,
        "params": {"ui": "storage"},
        'is_compleated': False
    },

    # 4) Zdeponuj iron ore do magazynu (20)
    "m_deposit_iron_20": {
        "title": "Dostawa do bazy",
        "desc": "Zdeponuj 20 rud żelaza do magazynu.",
        "type": "deposit_item",
        "target": 20,
        "params": {"item_id": "iron_ore"},
        'is_compleated': False
    },

    # 5) Przeleć dystans (200 jednostek)
    "m_travel_200": {
        "title": "Lot testowy",
        "desc": "Przeleć dystans 200 jednostek.",
        "type": "travel",
        "target": 200,
        "params": {"unit": "u"},
        'is_compleated': False
    },
}


def get_mission(mission_id: str) -> dict:
    return MISSIONS[mission_id]




