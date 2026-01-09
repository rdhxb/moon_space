from ..systems.inventory import Inventory

class Base():
    def __init__(self, tx, ty, capacity = 20):
        self.tx = tx
        self.ty = ty

        self.storage = Inventory(capacity)
        self.is_visible = False


    def depo_item(self, player_inv, item_id, qty):
        # ile mam 
        player_have = player_inv.count(item_id)
        # how many can move
        movable = min(qty, player_have)

        if movable <= 0 :
            return 0
        
    
        leftover = self.storage.add(item_id, movable)
        moved = movable - leftover
        if moved  > 0:
            player_inv.remove(item_id, moved)

        return moved
        
    def deposit_all(self, player_inv):
        moved_total = 0

        stacks = [s for s in player_inv.slots if s is not None and s.qty > 0]


        for s in stacks:
            moved_total += self.depo_item(player_inv, s.item_id, s.qty)

        return moved_total


        