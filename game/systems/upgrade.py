class UpgradeSystem():
    def __init__(self, player, storage):
        self.player = player
        self.storage = storage

        self.COSTS = {"backpack": {1: {"iron_ore": 1}, 2: {"iron_ore": 20}}, "mining": {1: {"iron_ore": 1}, 2: {"iron_ore": 20}}}


    def get_cost(self, upg_name):
        if upg_name == "backpack": 
            next_lvl = self.player.backpack_lvl + 1
        elif upg_name == "mining":
            next_lvl = self.player.mining_lvl + 1
        else:
            return None

        return self.COSTS.get(upg_name, {}).get(next_lvl) 


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

        # wymagany level gracza na następny poziom danego upgrade
        if upg_name == "backpack":
            required_lvl = self.player.backpack_lvl + 1
        elif upg_name == "mining":
            required_lvl = self.player.mining_lvl + 1
        else:
            return False

        if self.player.lvl < required_lvl:
            return False

        if not self.can_afford(cost):
            return False

        for item_id, need in cost.items():
            self.storage.remove(item_id, need)

        self.apply_upgrade(upg_name)
        return True

    def apply_upgrade(self,upgrade_name):
        if upgrade_name == "backpack":
            self.player.backpack_lvl += 1
            self.player.recalc_inventory_capacity()
        
        if upgrade_name == 'mining':
            self.player.mining_lvl += 1
