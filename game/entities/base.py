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
        moved_by_item = {}

        stacks = [s for s in player_inv.slots if s is not None and s.qty > 0]

        for s in stacks:
            moved = self.depo_item(player_inv, s.item_id, s.qty)
            if moved <= 0:
                continue

            moved_by_item[s.item_id] = moved_by_item.get(s.item_id, 0) + moved

        return moved_by_item


    def get_state(self):
        return {
            "tx": float(self.tx),
            "ty": float(self.ty),
            "storage": self.storage.get_state(),
        }

    def set_state(self, state: dict):
        if not isinstance(state, dict):
            return

        self.tx = float(state.get("tx", self.tx))
        self.ty = float(state.get("ty", self.ty))

        storage_state = state.get("storage")
        if isinstance(storage_state, dict) and hasattr(self.storage, "set_state"):
            self.storage.set_state(storage_state)

        