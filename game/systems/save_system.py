import json
import os
from pathlib import Path


class SaveSystem:
    def __init__(self, save_dir: str = "game/data/save"):
        self.save_dir = Path(save_dir)
        self.save_dir.mkdir(parents=True, exist_ok=True)

    def save_player(self, player_state, file_name: str = "player.json"):
        if not isinstance(player_state, dict):
            return

        path = self.save_dir / file_name
        tmp_path = self.save_dir / (file_name + ".tmp")

        data = {
            "version": 1,
            "player": player_state,
        }

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, path)

    def save_base(self, base_state, file_name: str = "base.json"):
        if not isinstance(base_state, dict):
            return

        path = self.save_dir / file_name
        tmp_path = self.save_dir / (file_name + ".tmp")

        data = {
            "version": 1,
            "base": base_state,
        }

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, path)


    
    def save_mission(self, mission_state, file_name: str = 'mission.json'):
        if not isinstance(mission_state, dict):
            return

        path = self.save_dir / file_name
        tmp_path = self.save_dir / (file_name + ".tmp")

        data = {
            "version": 1,
            "mission": mission_state,
        }

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, path)

    def save_shop(self, shop_state, file_name: str = 'shop.json'):
        if not isinstance(shop_state, dict):
            return

        path = self.save_dir / file_name
        tmp_path = self.save_dir / (file_name + ".tmp")

        data = {
            "version": 1,
            "shop": shop_state,
        }

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, path)

    def save_planet_manager(self, planet_manager, file_name: str = "planet.json"):
        if not isinstance(planet_manager, dict):
            return

        path = self.save_dir / file_name
        tmp_path = self.save_dir / (file_name + ".tmp")

        data = {
            "version": 1,
            "planet": planet_manager,
        }

        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        os.replace(tmp_path, path)


    

    def _load_section(self, file_name: str, key: str):
        path = self.save_dir / file_name
        if not path.exists():
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return None

        if not isinstance(data, dict):
            return None

        section = data.get(key)
        if not isinstance(section, dict):
            return None

        return section
    

    def load_player(self, file_name: str = "player.json"):
        return self._load_section(file_name, "player")
    
    def load_base(self, file_name: str = "base.json"):
        return self._load_section(file_name, "base")

    def load_mission(self, file_name: str = "mission.json"):
        return self._load_section(file_name, "mission")

    def load_shop(self, file_name: str = "shop.json"):
        return self._load_section(file_name, "shop")
    
    def load_planet_manager(self, file_name: str = "planet.json"):
        return self._load_section(file_name, "planet")







    def save_data(self, player_state, base_state, mission_state, shop_state, planet_state):
        self.save_player(player_state)
        self.save_base(base_state)
        self.save_mission(mission_state)
        self.save_shop(shop_state)
        self.save_planet_manager(planet_state)


    def load_data(self):
        return {
            "player": self.load_player(),
            "base": self.load_base(),
            "mission": self.load_mission(),
            "shop": self.load_shop(),      
        }


    def load_data_into(self, player=None, base=None, mission=None, shop=None):
        data = self.load_data()

        if player is not None:
            st = data.get("player")
            if isinstance(st, dict) and hasattr(player, "set_state"):
                player.set_state(st)

        if base is not None:
            st = data.get("base")
            if isinstance(st, dict) and hasattr(base, "set_state"):
                base.set_state(st)

        if mission is not None:
            st = data.get("mission")
            if isinstance(st, dict) and hasattr(mission, "set_state"):
                mission.set_state(st)

        if shop is not None:
            st = data.get("shop")
            if isinstance(st, dict) and hasattr(shop, "set_state"):
                shop.set_state(st)
        
        
