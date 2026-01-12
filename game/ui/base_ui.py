# base overlay ui with mission upgrade system inventory ect. i was wondering about bliting an img and then using bous to navigate and i think its a good idea class
import pygame
class BaseUI():
    def __init__(self, screen_w, screen_h):

        self.base_home_img = pygame.image.load('game/data/assets/base/base_home.png').convert_alpha()
        self.base_home_rect = self.base_home_img.get_rect()
        self.base_storage_img = pygame.image.load('game/data/assets/base/base_storage.png').convert_alpha()
        self.base_upgrade_img = pygame.image.load('game/data/assets/base/base_upgrade.png').convert_alpha()


        self.panel_w = 900
        self.panel_h = 600


        self.x, self.y = (screen_w - self.panel_w) // 2, (screen_h - self.panel_h) // 2 

        self.base_state = 'home'
        self.is_visible = False

        # przycimnienie tla 
        self.dim = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        self.dim.fill((0,0,0,140))

        self.font = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
        self.col_ok = (40, 200, 80)     # zielony
        self.col_no = (220, 60, 60)     # czerwony
        self.col_done = (30, 30, 30)    # czarny / ciemny
        self.col_white = (240, 240, 240)

        



    def open(self):
        self.is_visible = True
        self.base_state = 'home'
    
    def close(self):
        self.is_visible = False
    

    def handle_event(self, event, base, player, upg, mission):
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
                mission.on_ui_open('storage')
            elif event.key == pygame.K_u:
                self.base_state = "upgrade"
                
            elif event.key == pygame.K_q:
                self.base_state = "missions"
            
            if event.key == pygame.K_d and self.base_state == 'storage':
                moved = base.deposit_all(player.inventory)
                for item_id, qty in moved.items():
                    if qty > 0:
                        mission.on_item_depo(item_id, qty)

            if event.key == pygame.K_b and self.base_state == 'upgrade':
                upg.try_upgrade('backpack')

            if event.key == pygame.K_m and self.base_state == 'upgrade':
                upg.try_upgrade('mining')

        
    def draw(self,invui,base,player, screen : pygame.Surface, upgrade_sys):
        if not self.is_visible:
            return
        screen.blit(self.dim, (0, 0))

        if self.base_state == 'home':
            screen.blit(self.base_home_img,(self.x,self.y))
        if self.base_state == 'storage':
            screen.blit(self.base_storage_img,(self.x,self.y))
            invui.draw(screen,player.inventory,550,340 , 5)
            invui.draw(screen,base.storage,1000 ,340, 5)
        if self.base_state == 'upgrade':
            screen.blit(self.base_upgrade_img, (self.x, self.y))

            tx = self.x + 80
            backpact_ty = self.y + 140
            mining_ty = self.y + 140

            line_h = 34

 
            backpack_costs = upgrade_sys.COSTS.get("backpack", {})
            for lvl in sorted(backpack_costs.keys()):
                cost = backpack_costs[lvl]  

                status = self._upgrade_status("backpack", lvl, cost, player, base.storage)
                if status == "done":
                    color = self.col_done
                elif status == "available":
                    color = self.col_ok
                else:
                    color = self.col_no

                
                cost_txt = ", ".join([f"{need} {item_id}" for item_id, need in cost.items()])
                text = f"Backpack lvl {lvl} - {cost_txt} [B]"

                self._draw_upgrade_line(screen, text, color, tx, backpact_ty)
                backpact_ty += line_h


            mining_costs = upgrade_sys.COSTS.get("mining", {})
            for lvl in sorted(mining_costs.keys()):
                cost = mining_costs[lvl]  

                status = self._upgrade_status("mining", lvl, cost, player, base.storage)
                if status == "done":
                    color = self.col_done
                elif status == "available":
                    color = self.col_ok
                else:
                    color = self.col_no

                
                cost_txt = ", ".join([f"{need} {item_id}" for item_id, need in cost.items()])
                text = f"Mining lvl {lvl} - {cost_txt} [M]"

                self._draw_upgrade_line(screen, text, color, tx + 400 , mining_ty)
                mining_ty += line_h


    # upgrad hlper
    def _upgrade_status(self, upgrade_name, target_lvl, cost, player, storage):
    
        current = player.backpack_lvl if upgrade_name == "backpack" else player.mining_lvl
        if current >= target_lvl:
            return "done"

        for item_id, need in cost.items():
            if storage.count(item_id) < need:
                return "locked"
        return "available"
    
    def _draw_upgrade_line(self, screen, text, color, x, y):
        surf = self.font.render(text, True, color)
        screen.blit(surf, (x, y))