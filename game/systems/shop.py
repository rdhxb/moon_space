from ..data.items import ITEMS

class Shop:
    def __init__(self):
        self.items = ITEMS

    def sell(self, storage, item_id, qty, player):

        price = ITEMS[item_id].get("value", 0) if isinstance(ITEMS[item_id], dict) else ITEMS[item_id].value

        have = storage.count(item_id)

        to_sell = min(qty, have)

        sold = storage.remove(item_id, to_sell)
        earned = sold * price

        player.gold += earned
        print(sold, earned, player.gold)
        return sold, earned