from ..data.shop import SHOP
class Shop():
    def __init__(self):
        self.upgrades = SHOP
    
    def buy_upgrade(self, upg_name, player):     

        if upg_name == 'speed_upgrade' and self.can_afford(player, upg_name):
            player.base_speed += self.get_value(upg_name)
            player.gold -= self.get_price(upg_name)
            self.make_upg_more_expensive(upg_name)


        if upg_name == 'fuel_upg' and self.can_afford(player, upg_name):
            player.max_fuel += self.get_value(upg_name)
            player.gold -= self.get_price(upg_name)
            self.make_upg_more_expensive(upg_name)



    def get_price(self,upg_name):
        return self.upgrades[upg_name].get("price")
    
    def get_value(self, upg_name):
        return self.upgrades[upg_name].get("value")
    
    def make_upg_more_expensive(self,upg_name):
        upg = self.upgrades.get(upg_name)
        if not upg:
            return  

        price = upg.get("price", 0)
        upg["price"] = int(price * 1.5)

    def can_afford(self,player, upg_name):
        price = self.get_price(upg_name)
        current_p_gold = player.gold

        if current_p_gold - price >= 0:
            return True
        return False
    

    def get_state(self):
        prices = {}
        for name, upg in self.upgrades.items():
            if isinstance(upg, dict):
                prices[name] = int(upg.get("price", 0))

        return {
            "prices": prices
        }

    def set_state(self, state: dict):
        if not isinstance(state, dict):
            return

        self.upgrades = SHOP

        prices = state.get("prices", {})
        if not isinstance(prices, dict):
            return

        for name, price in prices.items():
            if name not in self.upgrades:
                continue
            try:
                self.upgrades[name]["price"] = int(price)
            except Exception:
                pass
