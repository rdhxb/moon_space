class UpgradeSystem():
    def __init__(self, player, storage, planet_id="moon"):
        self.player = player
        self.storage = storage
        self.planet_id = str(planet_id).lower()

        # te same nazwy upgrade, inne materiały per planeta
        self.COSTS_BY_PLANET = {
            "moon": {
                "backpack": {
                    1: {"iron_ore": 1},
                    2: {"iron_ore": 20},
                },
                "mining": {
                    1: {"iron_ore": 1},
                    2: {"iron_ore": 20},
                },
            },
            "mars": {
                "backpack": {
                    1: {"hematite_ore": 3},
                    2: {"hematite_ore": 25, "ferrosilicate_ore": 2},
                },
                "mining": {
                    1: {"hematite_ore": 3},
                    2: {"hematite_ore": 25, "ferrosilicate_ore": 2},
                },
            },
        }

    def set_planet(self, planet_id):
        self.planet_id = str(planet_id).lower()

    def _current_lvl(self, upg_name):
        if upg_name == "backpack":
            return self.player.backpack_lvl
        if upg_name == "mining":
            return self.player.mining_lvl
        return None

    def get_cost_table(self, upg_name):
        # tabela kosztów tylko dla aktualnej planety
        return self.COSTS_BY_PLANET.get(self.planet_id, {}).get(upg_name, {})

    def get_cost(self, upg_name):
        current = self._current_lvl(upg_name)
        if current is None:
            return None
        next_lvl = current + 1
        return self.get_cost_table(upg_name).get(next_lvl)

    def can_afford(self, cost):
        if not cost:
            return False
        for item_id, need in cost.items():
            if self.storage.count(item_id) < need:
                return False
        return True

    def try_upgrade(self, upg_name):
        cost = self.get_cost(upg_name)
        if cost is None:
            return False

        required_lvl = self._current_lvl(upg_name) + 1
        if self.player.lvl < required_lvl:
            return False

        if not self.can_afford(cost):
            return False

        for item_id, need in cost.items():
            self.storage.remove(item_id, need)

        self.apply_upgrade(upg_name)
        return True

    def apply_upgrade(self, upgrade_name):
        if upgrade_name == "backpack":
            self.player.backpack_lvl += 1
            self.player.recalc_inventory_capacity()
        elif upgrade_name == "mining":
            self.player.mining_lvl += 1
