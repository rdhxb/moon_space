import pygame
from ..entities.ship import Ship

pygame.init()

class Game():
    # init the variables 
    def __init__(self):
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.running = True
        self.color = (91,123,222)


        # self.world = WorldMap()
        self.player = Ship(self.width/2, self.height/2)
        # self.camera = Camera()
        # self.renderer = IsoRenderer()

    # draw everything on the screen like player world ect. 
    def draw(self):
        self.screen.fill(self.color)
        self.player.draw(self.screen)
        pygame.display.flip()
        # self.renderer.draw_world(self.screen, self.world, self.camera)

    # handle basic events like quit i dont know will it be more
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # upted the game like player world camera ect 
    def update(self):
        self.player.update()
        # self.camera.follow(self.player)
        self.clock.tick(self.FPS)
        pass

    # run the game just a funct
    def run(self):
        while self.running:
            
            self.handle_events()
            self.update()
            self.draw()



            

        
            
