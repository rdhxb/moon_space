import pygame
from ..entities.ship import Ship
from ..world.world_map import WorldMap
from ..render.TileSet import TileSet
from ..render.iso_render import IsoRender
from ..render.camera import Camera
from ..ui.hud import HUD
from ..data.items import validate_items

from ..ui.inventory_ui import INVUI

pygame.init()

class Game():
    # init the variables 
    def __init__(self):
        self.width = 1920     
        self.height = 1080
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.running = True
        self.color = (0,0,0)
        validate_items()


        self.world = WorldMap()
        self.tree = self.world.create_tree()
        self.iron_ore = self.world.create_iron_ores()
        cx = self.world.width_in_tiles  / 2
        cy = self.world.height_in_tiles / 2
        self.player = Ship(cx, cy)
        self.tile_set = TileSet()
        self.camera = Camera()
        self.renderer = IsoRender(self.world,self.camera, self.tile_set)

        self.game_state = 'play'
        self.near_base = False
        self.base_interaction_radius = 2.5

        self.font = pygame.font.SysFont('None', 24)
        self.hud = HUD(self.renderer,self.font)


        self.invui = INVUI(self.tile_set,self.width,self.height,self.player.inv_slots)

        self.near_ore = False
        self.ore_tile = None



    # draw everything on the screen like player world ect. 
    def draw(self):
        self.screen.fill(self.color)
        self.renderer.draw_world(self.screen)
        self.renderer.draw_sprites_helper(self.screen,'iron_ore_img','iron_ore_rect',self.world.iron_ores)
        self.player.draw(self.screen)
        
        self.renderer.draw_base(self.screen)
        # self.renderer.draw_trees(self.screen)
        self.renderer.draw_sprites_helper(self.screen,'tree_image','tree_rect',self.world.trees)
        self.hud.draw(self.screen, self.game_state, self.near_base)
        
        if self.near_ore:
            self.renderer.draw_ore_hint(self.screen, self.font, self.ore_tile, self.camera)


        if self.invui.is_visible:
            self.invui.draw(self.screen,self.player.inventory)



        pygame.display.flip()
        

    # handle basic events like quit i dont know will it be more
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.game_state == 'play':
                    if event.key == pygame.K_e and self.near_base:
                        self.game_state = 'base_menu'
                        print('Enter base menu')

                    if event.key == pygame.K_e and self.near_ore and self.ore_tile != None:
                        leftover = self.player.inventory.add('iron_ore', 55)
                        

                        if leftover == 0:
                            # znika po zebraniu
                            self.world.iron_ores.remove(self.ore_tile)
                            print('Zebrano rudę: +5 iron_ore')
                            # self.player.inventory.debug_print(self.player)

                        else:
                            print('Brak miejsca w inventory')
                            # self.player.inventory.debug_print(self.player)

                
                elif self.game_state == 'base_menu':
                    if event.key == pygame.K_e and self.near_base:
                        self.game_state = 'play'
                        print('Exit base menu enter play ')



                if event.key == pygame.K_i and self.invui.is_visible != True:
                    self.invui.is_visible = True
                elif event.key == pygame.K_i and self.invui.is_visible == True:
                    self.invui.is_visible = False


                


    # upted the game like player world camera ect 
    def update(self, dt):
        if self.game_state == 'play':
            self.player.update(dt,self.world)
            iso_x, iso_y = self.player.get_iso_pos(self.renderer.tile_w, self.renderer.tile_h)
            self.camera.center_on(iso_x, iso_y, self.width, self.height)
        
            # sprawdź, czy jesteśmy przy bazie
            self.is_near_base()
            self.is_near_ore()

        elif self.game_state == 'base_menu':
            # logika do bazy po wcisnieciu E
            # print('Enterint base menu to make moves in base ->><<-')
            pass

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

        if tile in self.world.iron_ores:
            self.near_ore = True
            self.ore_tile = tile
        else:
            self.near_ore = False
            self.ore_tile = None

        


    # run the game just a funct
    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()


    