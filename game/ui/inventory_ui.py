import pygame
class INVUI():
    def __init__(self, tile_set,w,h, inv_slots : int):
        self.tile_set = tile_set
        self.sx = w // 2
        self.sy = h // 2
        self.is_visible = False
        self.inv_slots = inv_slots
        self.inv_img = pygame.image.load('game/data/assets/invslot_64.png').convert_alpha()

        self.icons = {}
        self.icon_paths = {
            "iron_ore": "game/data/assets/iron_ore.png",
        }

        self.font = pygame.font.SysFont("Comic Sans MS", 22, italic=True)


    
    def draw(self,screen: pygame.Surface, inventory = None):
        # shift for every new block 
        left_shift = 32.5
        pos_x_after_shift = self.sx - (left_shift * self.inv_slots)

        for i in range(self.inv_slots):
            screen.blit(self.inv_img,(pos_x_after_shift + (64 * i),self.sy - 200))


        inv_slots = inventory.slots
        for i, slot in enumerate(inv_slots):
            if slot is None:
                continue

            item_id = slot.item_id
            item_qty = slot.qty

            # cache ikon
            if item_id not in self.icons:
                path = self.icon_paths.get(item_id)
                if path is None:
                    continue  # brak ikony dla tego itemu
                self.icons[item_id] = pygame.image.load(path).convert_alpha()

            icon = self.icons[item_id]

            # pozycja tego konkretnego slotu
            slot_x = pos_x_after_shift + (64 * i)
            slot_y = self.sy - 210

            # wycentruj ikonę w slocie
            ix = slot_x + (64 - icon.get_width()) // 2
            iy = slot_y + (64 - icon.get_height()) // 2
            screen.blit(icon, (ix, iy))
            screen.blit(self.font.render(f'{item_qty}x', False, "#BF0930CA"), (ix + 5,iy + 35))


