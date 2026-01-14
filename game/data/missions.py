MISSIONS = {
    # --- MOON (twoje) ---
    "m_collect_iron_5": {
        "title": "Pierwsza ruda",
        "desc": "Zbierz rudę żelaza.",
        "type": "collect_item",
        "target": 5,
        "params": {"item_id": "iron_ore"},
        "is_compleated": False,
        "planet": "moon",
    },
    "m_collect_iron_30": {
        "title": "Zapas na start",
        "desc": "Zbierz 30 rud żelaza.",
        "type": "collect_item",
        "target": 30,
        "params": {"item_id": "iron_ore"},
        "is_compleated": False,
        "planet": "moon",
    },
    "m_open_storage": {
        "title": "Pierwsza wizyta w magazynie",
        "desc": "Otwórz okno magazynu w bazie.",
        "type": "open_ui",
        "target": 1,
        "params": {"ui": "storage"},
        "is_compleated": False,
        "planet": "moon",
    },
    "m_deposit_iron_20": {
        "title": "Dostawa do bazy",
        "desc": "Zdeponuj 20 rud żelaza do magazynu.",
        "type": "deposit_item",
        "target": 20,
        "params": {"item_id": "iron_ore"},
        "is_compleated": False,
        "planet": "moon",
    },
    "m_travel_200": {
        "title": "Lot testowy",
        "desc": "Przeleć dystans 200 jednostek.",
        "type": "travel",
        "target": 200,
        "params": {"unit": "u"},
        "is_compleated": False,
        "planet": "moon",
    },

    # --- MARS ---
    "m_mars_collect_hematite_10": {
        "title": "Hematyt na rozruch",
        "desc": "Zbierz 10 rud hematytu.",
        "type": "collect_item",
        "target": 10,
        "params": {"item_id": "hematite_ore"},
        "is_compleated": False,
        "planet": "mars",
    },

    "m_mars_collect_ferrosilicate_8": {
        "title": "Twardsze złoża",
        "desc": "Zbierz 8 rud żelazokrzemianów.",
        "type": "collect_item",
        "target": 8,
        "params": {"item_id": "ferrosilicate_ore"},
        "is_compleated": False,
        "planet": "mars",
    },

    "m_mars_collect_sulfide_5": {
        "title": "Siarczkowe żyły",
        "desc": "Zbierz 5 rud siarczkowych.",
        "type": "collect_item",
        "target": 5,
        "params": {"item_id": "sulfide_ore"},
        "is_compleated": False,
        "planet": "mars",
    },

    "m_mars_deposit_hematite_15": {
        "title": "Zrzut surowca",
        "desc": "Zdeponuj 15 rud hematytu do magazynu w bazie.",
        "type": "deposit_item",
        "target": 15,
        "params": {"item_id": "hematite_ore"},
        "is_compleated": False,
        "planet": "mars",
    },

    "m_mars_travel_600": {
        "title": "Wyprawa zwiadowcza",
        "desc": "Przeleć dystans 600 jednostek na Marsie.",
        "type": "travel",
        "target": 600,
        "params": {"unit": "u"},
        "is_compleated": False,
        "planet": "mars",
    },

    "m_mars_open_storage": {
        "title": "Marsjański magazyn",
        "desc": "Otwórz magazyn w bazie po przylocie na Marsa.",
        "type": "open_ui",
        "target": 1,
        "params": {"ui": "storage"},
        "is_compleated": False,
        "planet": "mars",
    },
}



def get_mission(mission_id: str) -> dict:
    return MISSIONS[mission_id]




