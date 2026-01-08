import pygame
from ..world.world_map import WorldMap


class Ship():
    # init the variables 
    def __init__(self,x,y):

        self.tx = x
        self.ty = y

        self.tile_x = int(self.tx)
        self.tile_y = int(self.ty)

        self.width = 16
        self.height = 16

        self.speed = 5
        self.color = (255,0,255)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.ship_image = pygame.image.load('game/data/assets/ship.png').convert_alpha()
        self.ship_rect = self.ship_image.get_rect()



    def update(self,dt,world):
        old_tx, old_ty = self.tx, self.ty

        self.handle_input(dt)

        self.tile_x = int(self.tx)
        self.tile_y = int(self.ty)
        
        get_tile = world.get_tile(self.tile_x,self.tile_y)

        if get_tile == 1:
            self.tx, self.ty = old_tx, old_ty
            self.tile_x = int(self.tx)
            self.tile_y = int(self.ty)

        if (self.tile_x , self.tile_y) in world.trees:
            self.tx, self.ty = old_tx, old_ty
            self.tile_x = int(self.tx)
            self.tile_y = int(self.ty)





    def handle_input(self,dt):
        keys = pygame.key.get_pressed()
        # top bottom movement based on speed
        if keys[pygame.K_w]:
            self.ty -= self.speed * dt
        if keys[pygame.K_s]:
            self.ty += self.speed * dt
        # lef right movement based on speed  
        if keys[pygame.K_a]:
            self.tx -= self.speed * dt
        if keys[pygame.K_d]:
            self.tx += self.speed * dt

    # drawing ship on the screen based on x and y 
    def draw(self, surface : pygame.Surface):
        screen_w, screen_h = surface.get_size()
        ship_w = self.ship_image.get_width()
        ship_h = self.ship_image.get_height()

        draw_x = screen_w // 2 - ship_w // 2
        draw_y = screen_h // 2 - ship_h // 2

        surface.blit(self.ship_image,(draw_x,draw_y))
        


    def get_iso_pos(self,tile_w,tile_h):
        iso_x = (self.tx - self.ty) * (tile_w // 2)
        iso_y = (self.tx + self.ty) * (tile_h // 2)

        return iso_x , iso_y






