import pygame
from ..world.world_map import WorldMap
from math import sqrt, atan2, degrees, sin

class Ship():
    # init the variables 
    def __init__(self,x,y):

        self.tx = x
        self.ty = y

        self.tile_x = int(self.tx)
        self.tile_y = int(self.ty)

        self.width = 32
        self.height = 32

        self.speed = 5
        self.color = (255,0,255)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.ship_image = pygame.image.load('game/data/assets/ship.png').convert_alpha()
        self.ship_rect = self.ship_image.get_rect()

        # vector ruchu 
        self.vx = 0.0
        self.vy = 0.0
        # angle of drawing
        self.angle_deg = 0.0
        self.angle_target = 0.0
        self.rotation_speed = 300.0

        # idle gora dol w ruchu i w staniu
        # faza animacji 
        self.idle_phase = 0.0
        # jak szybko sie buja 
        self.idle_speed_while_still = 3.0
        self.idel_speed_in_move = 5.0
        # ile px gora dol
        self.idle_amplitude = 4.0


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


        # ship rotation using shortest path not faster then roptation speed 
        diff = (self.angle_target - self.angle_deg + 180) % 360 - 180

        max_step = self.rotation_speed * dt

        if diff > max_step:
            diff = max_step
        elif diff < -max_step:
            diff = -max_step

        self.angle_deg += diff






    def handle_input(self, dt):
        move_x = 0.0
        move_y = 0.0

        keys = pygame.key.get_pressed()

        # kierunki WASD -> wektor ruchu
        if keys[pygame.K_w]:
            move_y -= 1
        if keys[pygame.K_s]:
            move_y += 1
        if keys[pygame.K_a]:
            move_x -= 1
        if keys[pygame.K_d]:
            move_x += 1

        # brak ruchu
        if move_x == 0 and move_y == 0:
            self.vx = 0.0
            self.vy = 0.0
            self.idle_phase += self.idle_speed_while_still * dt
            return

        self.idle_phase += self.idel_speed_in_move * dt
        length = sqrt(move_x**2 + move_y**2)
        self.vx = move_x / length
        self.vy = move_y / length

        # ruch w świecie
        self.tx += self.vx * self.speed * dt
        self.ty += self.vy * self.speed * dt

        # obrot statku
        angle_rad = atan2(-self.vy, self.vx)  
        self.angle_target = degrees(angle_rad) + 225




    # drawing ship on the screen based on x and y 
    def draw(self, surface : pygame.Surface):
        offset_y = 0
        
        offset_y = sin(self.idle_phase) * self.idle_amplitude
        screen_w, screen_h = surface.get_size()
        rotated = pygame.transform.rotozoom(self.ship_image, self.angle_deg,1.5)
        rect = rotated.get_rect()
        rect.center = (screen_w // 2, screen_h // 2 + offset_y)
        surface.blit(rotated, rect.topleft)

        
        


    def get_iso_pos(self,tile_w,tile_h):
        iso_x = (self.tx - self.ty) * (tile_w // 2)
        iso_y = (self.tx + self.ty) * (tile_h // 2)

        return iso_x , iso_y






