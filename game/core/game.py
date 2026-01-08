import pygame
from ..entities.ship import Ship
from ..world.world_map import WorldMap
from ..render.TileSet import TileSet
from ..render.iso_render import IsoRender
from ..render.camera import Camera
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



        self.world = WorldMap()
        self.tree = self.world.create_tree()
        cx = self.world.width_in_tiles  / 2
        cy = self.world.height_in_tiles / 2
        self.player = Ship(cx, cy)
        self.tile_set = TileSet()
        self.camera = Camera()
        self.renderer = IsoRender(self.world,self.camera, self.tile_set)

        self.game_state = 'play'
        self.near_base = 'False'
        self.base_interaction_radius = 2.5

        self.font = pygame.font.SysFont('None', 24)

        


    # draw everything on the screen like player world ect. 
    def draw(self):
        self.screen.fill(self.color)
        self.renderer.draw_world(self.screen)
        self.player.draw(self.screen)
        
        self.renderer.draw_base(self.screen)
        self.renderer.draw_trees(self.screen)

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
                
                elif self.game_state == 'base_menu':
                    if event.key == pygame.K_e and self.near_base:
                        self.game_state = 'play'
                        print('Exit base menu enter play ')

                


    # upted the game like player world camera ect 
    def update(self, dt):
        if self.game_state == 'play':
            self.player.update(dt,self.world)
            iso_x, iso_y = self.player.get_iso_pos(self.renderer.tile_w, self.renderer.tile_h)
            self.camera.center_on(iso_x, iso_y, self.width, self.height)
        
            # sprawdź, czy jesteśmy przy bazie
            self.is_near_base()

        elif self.game_state == 'base_menu':
            # logika do bazy po wcisnieciu E
            print('Enterint base menu to make moves in base ->><<-')
            pass

    def is_near_base(self):
        base_tx, base_ty = self.world.base_pos
        px,py = self.player.tile_x, self.player.tile_y

        dx = px - base_tx -  1
        dy = py - base_ty - 2

        self.near_base = (abs(dx) <= self.base_interaction_radius) and (abs(dy) <= self.base_interaction_radius)
        print(f'self near base var -> {self.near_base} base_tx -> {base_tx} base_ty -> {base_ty} player_x -> {px} player_y -> {py}')


    # run the game just a funct
    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()


    