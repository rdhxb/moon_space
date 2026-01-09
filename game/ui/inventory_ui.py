import pygame
class INVUI():
    def __init__(self, tile_set,w,h, inv_slots : int):
        self.tile_set = tile_set
        self.sx = w // 2
        self.sy = h // 2
        self.is_visible = False
        self.inv_slots = inv_slots
        self.inv_img = pygame.image.load('game/data/assets/invslot_64.png').convert_alpha()

    
    def draw(self,screen: pygame.Surface, inventory = None):
        # shift for every new block 
        left_shift = 32.5
        pos_x_after_shift = self.sx - (left_shift * self.inv_slots)

        for i in range(self.inv_slots):
            screen.blit(self.inv_img,(pos_x_after_shift + (64 * i),self.sy - 200))

