# base overlay ui with mission upgrade system inventory ect. i was wondering about bliting an img and then using bous to navigate and i think its a good idea class
import pygame
class BaseUI():
    def __init__(self, screen_w, screen_h):

        self.base_home_img = pygame.image.load('game/data/assets/base/base_home.png').convert_alpha()
        self.base_home_rect = self.base_home_img.get_rect()
        self.base_storage_img = pygame.image.load('game/data/assets/base/base_storage.png').convert_alpha()


        self.panel_w = 900
        self.panel_h = 600


        self.x, self.y = (screen_w - self.panel_w) // 2, (screen_h - self.panel_h) // 2 

        self.base_state = 'home'
        self.is_visible = False

        # przycimnienie tla 
        self.dim = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        self.dim.fill((0,0,0,140))



    def open(self):
        self.is_visible = True
        self.base_state = 'home'
    
    def close(self):
        self.is_visible = False
    

    def handle_event(self, event, base, player):
        if not self.is_visible:
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_e):
                if self.base_state == "home":
                    
                    self.close()  
                else:
                    self.base_state = "home"
            elif event.key == pygame.K_p:
                self.base_state = "storage"
            elif event.key == pygame.K_u:
                self.base_state = "upgrade"
            elif event.key == pygame.K_q:
                self.base_state = "missions"
            
            if event.key == pygame.K_d and self.base_state == 'storage':
                base.deposit_all(player.inventory)

        
    def draw(self,invui,base,player, screen : pygame.Surface):
        if not self.is_visible:
            return
        screen.blit(self.dim, (0, 0))

        if self.base_state == 'home':
            screen.blit(self.base_home_img,(self.x,self.y))
        if self.base_state == 'storage':
            screen.blit(self.base_storage_img,(self.x,self.y))
            invui.draw(screen,player.inventory,550,340 , 5)
            invui.draw(screen,base.storage,1000 ,340, 5)