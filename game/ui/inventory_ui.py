import pygame
class INVUI():
    def __init__(self, tile_set,w,h):
        self.tile_set = tile_set
        self.sx = w // 2
        self.sy = h // 2
        self.is_visible = False
        self.inv_img = pygame.image.load('game/data/assets/invslot_64.png').convert_alpha()

        self.icons = {}
        self.icon_paths = {
            "iron_ore": "game/data/assets/iron_ore.png",

            # mars ores
            "hematite_ore": "game/data/assets/Red_crystal4.png",    
            "ferrosilicate_ore": "game/data/assets/Violet_crystal4.png",
            "sulfide_ore": "game/data/assets/Yellow-green_crystal4.png",
        }

        self.font = pygame.font.SysFont("Comic Sans MS", 22, italic=True)


    
    def draw(self,screen: pygame.Surface, inventory, x, y, cols, return_rect = False):
        inv_slots = len(inventory.slots)


        slot_w = self.inv_img.get_width()
        slot_h = self.inv_img.get_height()
        gap = 10
        rows = (inv_slots + cols - 1) // cols

        rects = [] if return_rect  else None

        for i in range(min(len(inventory.slots), cols * rows)):
            col = i % cols
            row = i // cols
            slot_x = x + col * (slot_w + gap)
            slot_y = y + row * (slot_h + gap)

            screen.blit(self.inv_img,(slot_x,slot_y))

            if return_rect:
                rects.append(pygame.Rect(slot_x, slot_y, slot_w, slot_h))



        for i, slot in enumerate(inventory.slots):
            if slot is None:
                continue

            item_id = slot.item_id
            item_qty = slot.qty

            if item_id not in self.icons:
                path = self.icon_paths.get(item_id)
                if path is None:
                    continue
                self.icons[item_id] = pygame.image.load(path).convert_alpha()

            icon = self.icons[item_id]

            col = i % cols
            row = i // cols
            slot_x = x + col * (slot_w + gap)
            slot_y = y + row * (slot_h + gap)

            ix = slot_x + (slot_w - icon.get_width()) // 2
            iy = slot_y + (slot_h - icon.get_height()) // 2
            screen.blit(icon, (ix, iy))
            screen.blit(self.font.render(f'{item_qty}x', False, (191, 9, 48)), (slot_x + 6, slot_y + slot_h - 24))

        return rects
