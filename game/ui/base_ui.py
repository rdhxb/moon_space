# base overlay ui with mission upgrade system inventory ect. i was wondering about bliting an img and then using bous to navigate and i think its a good idea class
import pygame
from ..data.items import ITEMS
class BaseUI():
    def __init__(self, screen_w, screen_h):

        self.base_home_img = pygame.image.load('game/data/assets/base/base_home.png').convert_alpha()
        self.base_home_rect = self.base_home_img.get_rect()
        self.base_storage_img = pygame.image.load('game/data/assets/base/base_storage.png').convert_alpha()
        self.base_upgrade_img = pygame.image.load('game/data/assets/base/base_upgrade.png').convert_alpha()
        self.base_mission_img = pygame.image.load('game/data/assets/base/base_mission.png').convert_alpha()
        self.base_shop_img = pygame.image.load('game/data/assets/base/base_shop.png').convert_alpha()


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

        self.col_hint = (235, 235, 235)
        self.col_hint_dim = (180, 180, 180)
        
        self.col_in_progress = (240, 240, 240)  # biały
        self.col_done_mission = (40, 200, 80)   # zielony (albo szary jeśli wolisz)

        # index in stack 
        self.shop_selected_item = 0
        self.shop_qty = 0
        self.shop_msg = ''
        self.shop_item_qty = False
        self.shop_item_id = None

        self.items = ITEMS



    def open(self):
        self.is_visible = True
        self.base_state = 'home'
    
    def close(self):
        self.is_visible = False
    

    def handle_event(self, event, base, player, upg, mission, shop):
        if not self.is_visible:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
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
            elif event.key == pygame.K_s:
                self.base_state = 'shop'
                
            
            if event.key == pygame.K_d and self.base_state == 'storage':
                moved = base.deposit_all(player.inventory)
                for item_id, qty in moved.items():
                    if qty > 0:
                        mission.on_item_depo(item_id, qty)

            if event.key == pygame.K_b and self.base_state == 'upgrade':
                upg.try_upgrade('backpack')

            if event.key == pygame.K_m and self.base_state == 'upgrade':
                upg.try_upgrade('mining')

            if self.base_state == 'shop' and self.shop_item_qty == False:
                if event.key == pygame.K_RIGHT:
                    self.shop_selected_item += 1
                if event.key == pygame.K_LEFT and self.shop_selected_item >=1:
                    self.shop_selected_item -= 1
                if event.key == pygame.K_DOWN:
                    self.shop_selected_item += 5
                if event.key == pygame.K_UP and self.shop_selected_item >= 5:
                    self.shop_selected_item -= 5

                if event.key == pygame.K_SPACE:
                    slot = base.storage.slots[self.shop_selected_item]
                    if slot is None:
                        return  # albo po prostu nic nie rób
                    self.shop_item_qty = True
                    self.shop_item_id = slot.item_id
                    self.shop_qty = 1
            if event.key == pygame.K_ESCAPE and self.base_state == 'shop':
                self.shop_item_qty = False
                
            if self.shop_item_qty:
                if event.key == pygame.K_RIGHT:
                    self.shop_qty += 1
                elif event.key == pygame.K_LEFT:
                    self.shop_qty -= 1
                elif event.key == pygame.K_UP:
                    self.shop_qty += 5
                
            max_have = base.storage.count(self.shop_item_id)
            if self.shop_qty > max_have:
                self.shop_qty = max_have
                
            if self.shop_item_qty and event.key == pygame.K_RETURN:
                sold, earned = shop.sell(base.storage, self.shop_item_id, self.shop_qty, player)
                self.shop_item_qty = False
                self.shop_item_id = None
                self.shop_qty = 1

                        
                    

        
    def draw(self,invui,base,player, screen : pygame.Surface, upgrade_sys, missions):
        if not self.is_visible:
            return
        screen.blit(self.dim, (0, 0))

        if self.base_state == 'home':
            screen.blit(self.base_home_img,(self.x,self.y))

        if self.base_state == 'storage':
            screen.blit(self.base_storage_img,(self.x,self.y))
            invui.draw(screen,player.inventory,550,340 , 5)
            invui.draw(screen,base.storage,1000 ,340, 5)

        if self.base_state == 'missions':
            screen.blit(self.base_mission_img,(self.x,self.y))
            self.draw_missions(screen, missions)

        if self.base_state == 'shop':
            screen.blit(self.base_shop_img,(self.x,self.y))
            storage_rects = invui.draw(screen,base.storage,self.x + 500 ,self.y + 120 , 5, return_rect = True)
            if storage_rects:
                idx = self.shop_selected_item
                if 0 <= idx < len(storage_rects):
                    pygame.draw.rect(screen, (255, 255, 0), storage_rects[idx], 3, border_radius=6)
            self.draw_shop_hints(base,self.items,screen)



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
        
        if player.lvl < target_lvl:
            return 'locked'

        for item_id, need in cost.items():
            if storage.count(item_id) < need:
                return "locked"
        return "available"
    
    def _draw_upgrade_line(self, screen, text, color, x, y):
        surf = self.font.render(text, True, color)
        screen.blit(surf, (x, y))

    
    def draw_missions(self,screen,missions):
        x = self.x + 80
        y = self.y + 140
        line_h = 30

        for mission_id, row in missions.iter_rows():
            title, prog, target, done = row

            if done:
                color = self.col_done_mission
                text = f"{title}  DONE"
            else:
                color = self.col_in_progress
                # prog może być float
                if isinstance(prog, float):
                    p = int(prog)
                else:
                    p, t = prog, target
                text = f"{title}: {p}/{t}"

            surf = self.font.render(text, True, color)
            screen.blit(surf, (x, y))
            y += line_h

    def draw_shop_hints(self, base, ITEMS, screen ,):
        hx = self.x + 70
        hy = self.y + 260
        lh = 22

        lines = []

        if not self.shop_item_qty:
            lines.append(("SHOP", self.col_hint))
            lines.append(("Select slot: Arrow keys", self.col_hint))
            lines.append(("Accept slot: SPACE", self.col_hint))
            lines.append(("Sell: ENTER (after choosing qty)", self.col_hint_dim))
        else:
            lines.append(("SHOP", self.col_hint))
            lines.append(("Select qty: LEFT / RIGHT", self.col_hint))
            lines.append(("Sell: ENTER", self.col_hint))
            lines.append(("Cancel: ESC", self.col_hint_dim))

        
        profit_line = None
        if self.shop_item_id:
            
            have = base.storage.count(self.shop_item_id)
            qty = max(1, min(self.shop_qty, have))

            
            price = ITEMS[self.shop_item_id]["value"] 
            earned = qty * price

            profit_line = f"Selected: {self.shop_item_id} | Qty: {qty} | Earn: {earned}g"

        for i, (txt, col) in enumerate(lines):
            screen.blit(self.font.render(txt, True, col), (hx, hy + i * lh))

        if profit_line:
            screen.blit(self.font.render(profit_line, True, self.col_hint), (hx, hy + len(lines) * lh + 6))
