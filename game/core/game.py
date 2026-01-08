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


    # upted the game like player world camera ect 
    def update(self, dt):
        self.player.update(dt,self.world)

        iso_x, iso_y = self.player.get_iso_pos(self.renderer.tile_w, self.renderer.tile_h)
        self.camera.center_on(iso_x, iso_y, self.width, self.height)


        dx = 0
        dy = 0
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            dx += self.camera.camera_speed * dt 
        if keys[pygame.K_LEFT]:
            dx -= self.camera.camera_speed * dt 
        if keys[pygame.K_UP]:
            dy -= self.camera.camera_speed * dt 
        if keys[pygame.K_DOWN]:
            dy += self.camera.camera_speed * dt 

        self.camera.move(dx,dy)


    # run the game just a funct
    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
