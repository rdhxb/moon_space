import pygame
from ..entities.ship import Ship
from ..world.world_map import WorldMap
from ..render.TileSets import MoonTileSet, MarsTileSet
from ..render.iso_render import IsoRender
from ..render.camera import Camera
from ..ui.hud import HUD
from ..data.items import validate_items
from ..entities.base import Base
from ..systems.upgrade import UpgradeSystem

from ..ui.inventory_ui import INVUI
from ..ui.base_ui import BaseUI

from ..systems.missions import MissionTracker

from ..ui.player_ui import PlayerUI

from ..systems.cantor import Cantor
from ..ui.tutorial import Tutorial
from ..systems.planet_menageer import PlanetManager

from ..world.planets import build_world

from ..systems.shop import Shop
pygame.init()

class Game():
    # init the variables 
    def __init__(self):
        self.width = 1920     
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.FPS = 60
        self.clock = pygame.time.Clock()
        
        pygame.mixer.music.load('game/data/assets/space.mp3')
        pygame.mixer.music.play(-1)

        self.pick_up_sound = pygame.mixer.Sound('game/data/assets/item-pickup.mp3')
        

        self.running = True
        self.color = (0,0,0)
        validate_items()

        self.world = build_world('moon')


        cx = self.world.width_in_tiles  / 2
        cy = self.world.height_in_tiles / 2
        self.player = Ship(cx, cy)

        self.tile_set = MoonTileSet()
        self.camera = Camera()

        self.renderer = IsoRender(self.world, self.camera, self.tile_set)

        self.game_state = 'play'
        self.near_base = False
        self.base_interaction_radius = 2.5

        self.font = pygame.font.SysFont('None', 24)
        self.hud = HUD(self.renderer,self.font)


        self.invui = INVUI(self.tile_set,self.width,self.height)

        self.near_ore = False
        self.ore_tile = None

        # pozycja bazy z world 
        bx,by = self.world.base_pos
        self.base = Base(bx, by, 30)

        self.is_base_storge_open = False

        
        

        self.base_ui = BaseUI(self.width, self.height)

        self.mission = MissionTracker(self.player)

        self.prev_tx = self.player.tx
        self.prev_ty = self.player.ty

        self.player_ui = PlayerUI()
        self.cantor = Cantor()

        self.tutuorial = Tutorial(self.width,self.height)

        self.planet_menager = PlanetManager()
        self.upgrade = UpgradeSystem(self.player,self.base.storage, self.planet_menager.current_id)

        self.shop = Shop()

        self.near_obj_tile = None
        self.near_obj_type = None 

        self.mineable_types = {
            "ore_iron",
            "red_hematite_ore",
            "ferrosilicate_ore",
            "sulfide_vein_ore",
        }




    # draw everything on the screen like player world ect. 
    def draw(self):
        self.screen.fill(self.color)
        self.renderer.draw_world(self.screen)
        self.renderer.draw_objects(self.screen, self.world.objects_by_type)

        self.player.draw(self.screen)
        
        self.renderer.draw_base(self.screen)
        self.hud.draw(self.screen, self.game_state, self.near_base)
        
        if self.near_ore:
            self.renderer.draw_ore_hint(self.screen, self.font, self.ore_tile, self.camera)


        if self.invui.is_visible and self.base.is_visible == False:
            self.invui.draw(self.screen,self.player.inventory,self.width//2 - (32.5 * self.player.inv_slots),(self.height // 2) - 200 , 6)


        self.base_ui.draw(self.invui,self.base,self.player,self.screen,self.upgrade,self.mission, self.shop)

        self.player_ui.draw_player_current_stats(self.screen,self.font,self.player)

        self.tutuorial.draw(self.screen, self.planet_menager.current_id)

        pygame.display.flip()
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.game_state == 'play':
                    if event.key == pygame.K_e and self.near_base:
                        self.game_state = 'base_menu'
                        self.base_ui.open()
                        self.player.fuel = self.player.max_fuel

                    if event.key == pygame.K_e and self.near_ore and self.ore_tile is not None and self.near_obj_type is not None:
                        qty_to_pick = (1 * self.player.mining_lvl) + 1
                        

                        sprite_to_item = {
                            "ore_iron": "iron_ore",
                            "red_hematite_ore": "hematite_ore",
                            "ferrosilicate_ore": "ferrosilicate_ore",
                            "sulfide_vein_ore": "sulfide_ore",
                        }

                        item_id = sprite_to_item.get(self.near_obj_type, "iron_ore")

                        leftover = self.player.inventory.add(item_id, qty_to_pick)
                        moved = qty_to_pick - leftover

                        if moved > 0:
                            self.world.objects_by_type[self.near_obj_type].remove(self.ore_tile)
                            self.mission.on_item_collected(item_id, qty_to_pick)
                            self.pick_up_sound.play()
                        else:
                            print("Brak miejsca w inventory")

                    
                    if event.key == pygame.K_i and self.invui.is_visible != True:
                        self.invui.is_visible = True
                    elif event.key == pygame.K_i and self.invui.is_visible == True:
                        self.invui.is_visible = False
                    
                    if event.key == pygame.K_t and self.tutuorial.is_visible != False:
                        self.tutuorial.is_visible = False

                    elif event.key == pygame.K_t and self.tutuorial.is_visible == False:
                        self.tutuorial.is_visible = True

                    if event.key == pygame.K_1:
                        if self.planet_menager.try_unlock(self.mission.compleated_count):
                            self.load_planet('mars')
                
                elif self.game_state == 'base_menu':
                    self.base_ui.handle_event(event,self.base, self.player,self.upgrade, self.mission, self.cantor, self.shop)
                    if self.game_state == "base_menu" and not self.base_ui.is_visible:
                        self.game_state = "play"




    # upted the game like player world camera ect 
    def update(self, dt):
        if self.game_state == 'play':
            self.player.update(dt,self.world)
            self.world.center_tx = int(self.player.tx)
            self.world.center_ty = int(self.player.ty)
            iso_x, iso_y = self.player.get_iso_pos(self.renderer.tile_w, self.renderer.tile_h)
            self.camera.center_on(iso_x, iso_y, self.width, self.height)
        
            # sprawdź, czy jesteśmy przy bazie
            self.is_near_base()

            self.is_near_ore()

            self.distance_count()
            


    def is_near_base(self):
        base_tx, base_ty = self.world.base_pos
        px,py = self.player.tx, self.player.ty

        dx = px - base_tx 
        dy = py - base_ty

        self.near_base = (abs(dx) <= self.base_interaction_radius) and (abs(dy) <= self.base_interaction_radius)
        # print(f'self near base var -> {self.near_base} base_tx -> {base_tx} base_ty -> {base_ty} player_x -> {px} player_y -> {py}')

    def is_near_ore(self):
        px, py = self.player.tile_x, self.player.tile_y
        tile = (px, py)

        self.near_ore = False
        self.ore_tile = None
        self.near_obj_type = None

        objects = getattr(self.world, "objects_by_type", None)
        if not objects:
            return

        for t in self.mineable_types:
            positions = objects.get(t)
            if positions and tile in positions:
                self.near_ore = True
                self.ore_tile = tile
                self.near_obj_type = t
                return


    def distance_count(self):
        dx = self.player.tx - self.prev_tx
        dy = self.player.ty - self.prev_ty
        dist = (dx*dx + dy*dy) ** 0.5

        if dist > 0:
            self.mission.on_distance(dist)

        self.prev_tx = self.player.tx
        self.prev_ty = self.player.ty

        
    def load_planet(self, planet_id):
        self.world = build_world(planet_id)

        if planet_id == "mars":
            self.tile_set = MarsTileSet()
        else:
            self.tile_set = MoonTileSet()

        self.player.lvl = 1
        self.player.backpack_lvl = 0
        self.player.mining_lvl = 0
        self.player.recalc_inventory_capacity()
        
        self.renderer = IsoRender(self.world, self.camera, self.tile_set)

        
        self.hud.renderer = self.renderer
        self.invui = INVUI(self.tile_set, self.width, self.height)
        self.tutuorial.is_visible = True

        # baza (po world)
        bx, by = self.world.base_pos
        self.base = Base(bx, by, 30)
        self.upgrade = UpgradeSystem(self.player, self.base.storage,planet_id)

        # teleport gracza obok bazy
        self.player.tx = bx + 1
        self.player.ty = by + 1
        self.player.tile_x = int(self.player.tx)
        self.player.tile_y = int(self.player.ty)

        # reset stanów interakcji
        self.near_base = False
        self.near_ore = False
        self.ore_tile = None
        self.near_obj_type = None

        self.prev_tx = self.player.tx
        self.prev_ty = self.player.ty

        # UI state
        self.base_ui.close()
        self.invui.is_visible = False
        self.game_state = "play"

        # kamera na gracza
        iso_x, iso_y = self.player.get_iso_pos(self.renderer.tile_w, self.renderer.tile_h)
        self.camera.center_on(iso_x, iso_y, self.width, self.height)

        # misje / planet manager
        self.mission = MissionTracker(self.player)
        self.mission.set_planet(planet_id)
        self.planet_menager.set_current(planet_id)


    # run the game just a funct
    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()



    