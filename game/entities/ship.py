import pygame
from ..world.world_map import WorldMap
from math import sqrt, atan2, degrees, sin
from ..systems.inventory import Inventory
class Ship():
    # init the variables 
    def __init__(self,x,y):

        self.tx = x
        self.ty = y

        self.tile_x = int(self.tx)
        self.tile_y = int(self.ty)

        self.width = 32
        self.height = 32

        self.base_speed = 5
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
        # backpack level (inv slots)
        self.backpack_lvl = 0
        self.inv_slots = (1 * self.backpack_lvl) + 1
        # mining level
        self.mining_lvl = 0

        self.inventory = Inventory(self.inv_slots)
        # player overall level need for upgrade and tings like this earnin by doing qests 
        self.lvl = 1

        self.gold: int = 0
        self._rot_cache = {}          
        self._last_angle_step = None
        self._angle_step_deg = 3    
        self._scale = 1.5

        self.max_fuel = 10
        self.fuel = self.max_fuel
        self.fuel_burn_per_px = 0.05



    def update(self, dt, world):
        old_tx, old_ty = self.tx, self.ty

        self.handle_input(dt)

        test_tx = self.tx
        test_ty = old_ty
        if world.is_blocked(int(test_tx), int(test_ty)):
            self.tx = old_tx

        test_tx = self.tx
        test_ty = self.ty
        if world.is_blocked(int(test_tx), int(test_ty)):
            self.ty = old_ty

        self.tile_x = int(self.tx)
        self.tile_y = int(self.ty)

        diff = (self.angle_target - self.angle_deg + 180) % 360 - 180
        max_step = self.rotation_speed * dt
        if diff > max_step:
            diff = max_step
        elif diff < -max_step:
            diff = -max_step
        self.angle_deg += diff

        dx = self.tx - old_tx
        dy = self.ty - old_ty
        dist = (dx*dx + dy*dy) ** 0.5

        if dist > 0:
            burn = dist * self.fuel_burn_per_px
            self.fuel = max(0, self.fuel - burn)

        if self.fuel == 0:
            self.speed = 2
        else:
            self.speed = self.base_speed







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
    def draw(self, surface: pygame.Surface):
        offset_y = sin(self.idle_phase) * self.idle_amplitude

        screen_w, screen_h = surface.get_size()

        # kwantyzacja kąta (np. co 5°)
        angle_step = int(round(self.angle_deg / self._angle_step_deg)) * self._angle_step_deg
        angle_step %= 360

        rotated = self._rot_cache.get(angle_step)
        if rotated is None:
            rotated = pygame.transform.rotozoom(self.ship_image, angle_step, self._scale)
            self._rot_cache[angle_step] = rotated

        rect = rotated.get_rect()
        rect.center = (screen_w // 2, screen_h // 2 + offset_y)
        surface.blit(rotated, rect.topleft)

        


    def get_iso_pos(self,tile_w,tile_h):
        iso_x = (self.tx - self.ty) * (tile_w // 2)
        iso_y = (self.tx + self.ty) * (tile_h // 2)

        return iso_x , iso_y



    def recalc_inventory_capacity(self):
        self.inv_slots = (1 * self.backpack_lvl) + 1
        self.inventory.resize(self.inv_slots)
