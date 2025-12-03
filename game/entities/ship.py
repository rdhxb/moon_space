import pygame


class Ship():
    # init the variables 
    def __init__(self,x,y):

        self.x = x
        self.y = y

        self.width = 32
        self.height = 32

        self.speed = 4
        self.color = (255,0,255)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.update_rect()


    # set rect on the right pos 
    def update_rect(self):
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def update(self):
        self.handle_input()
        self.update_rect()

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # top bottom movement based on speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        # lef right movement based on speed  
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

    # drawing ship on the screen based on x and y 
    def draw(self, surface : pygame.Surface):
        draw_x = self.rect.x
        draw_y = self.rect.y

        pygame.draw.rect(surface, self.color, (draw_x, draw_y, self.width, self.height))







