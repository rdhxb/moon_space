import pygame
from ..world.world_map import WorldMap


class Ship():
    # init the variables 
    def __init__(self,x,y):

        self.tx = x
        self.ty = y

        self.width = 16
        self.height = 16

        self.speed = 0.1
        self.color = (255,0,255)

        self.rect = pygame.Rect(0,0,self.width,self.height)



    def update(self):
        self.handle_input()



    def handle_input(self):
        keys = pygame.key.get_pressed()
        # top bottom movement based on speed
        if keys[pygame.K_w]:
            self.ty -= self.speed
            print(self.tx,self.ty)
        if keys[pygame.K_s]:
            self.ty += self.speed
        # lef right movement based on speed  
        if keys[pygame.K_a]:
            self.tx -= self.speed
        if keys[pygame.K_d]:
            self.tx += self.speed

    # drawing ship on the screen based on x and y 
    def draw(self, surface : pygame.Surface):
        screen_w, screen_h = surface.get_size()
        draw_x = screen_w // 2 - self.width // 2
        draw_y = screen_h // 2 - self.height // 2
        pygame.draw.rect(surface, self.color, (draw_x, draw_y, self.width, self.height))


    def get_iso_pos(self,tile_w,tile_h):
        iso_x = (self.tx - self.ty) * (tile_w // 2)
        iso_y = (self.tx + self.ty) * (tile_h // 2)

        return iso_x , iso_y






