from ..data.items import stack_max

class Inventory:
    def __init__(self, capacity=4):
        self.capacity = capacity
        self.slots = [None] * self.capacity

    def add(self, item_id, qty):
        leftover = qty

        # dodaj do istniejacych stackow
        for stack in self.slots:
            if stack is None:
                continue
            if stack.item_id != item_id:
                continue
            if leftover <= 0:
                break

            added = stack.add(leftover)
            leftover -= added

        # dodaj w puste sloty
        for i in range(self.capacity):
            if leftover <= 0:
                break
            if self.slots[i] is not None:
                continue

            new_stack = ItemStack(item_id, 0)
            added = new_stack.add(leftover)
            self.slots[i] = new_stack
            leftover -= added

        return leftover

    def remove(self, item_id, qty):
        # zwraca removed (ile faktycznie usunięto)
        if qty <= 0:
            return 0

        leftover = qty
        removed_total = 0

        for i in range(self.capacity):
            stack = self.slots[i]
            if stack is None:
                continue
            if stack.item_id != item_id:
                continue
            if leftover <= 0:
                break

            removed = stack.remove(leftover)
            removed_total += removed
            leftover -= removed

            if stack.qty <= 0:
                self.slots[i] = None

        return removed_total

    def count(self, item_id):
        total = 0
        for stack in self.slots:
            if stack and stack.item_id == item_id:
                total += stack.qty
        return total

    def has(self, item_id, qty):
        return self.count(item_id) >= qty
    
    def iter_stacks(self):
        for i in self.slots:
            if i is not None and i.qty > 0:
                yield i

    def used_slots(self):
        return sum(1 for s in self.slots if s is not None and s.qty > 0)
    

    def debug_print(self,player):
        for i, stack in enumerate(player.inventory.slots):
            if stack is None:
                continue
            print(f'Aktualny stan plecaka - > slot: {i}, item_id: {stack.item_id}, ilosc: {stack.qty}')






class ItemStack:
    def __init__(self, item_id, qty=0):
        self.item_id = item_id
        self.qty = qty

    def max_qty(self):
        return stack_max(self.item_id)

    def space_left(self):
        return self.max_qty() - self.qty

    def add(self, amount):
        add_now = min(amount, self.space_left())
        self.qty += add_now
        return add_now

    def remove(self, amount):
        rem_now = min(amount, self.qty)
        self.qty -= rem_now
        return rem_now
            
    
    
    


        





