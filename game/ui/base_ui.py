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
        self.base_cantor_img = pygame.image.load('game/data/assets/base/base_shop.png').convert_alpha()


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
        self.cantor_selected_item = 0
        self.cantor_qty = 0
        self.cantor_msg = ''
        self.cantor_item_qty = False
        self.cantor_item_id = None

        self.items = ITEMS

        self.gold_selected_idx = 0
        self.gold_msg = ""
        self.gold_msg_until = 0



    def open(self):
        self.is_visible = True
        self.base_state = 'home'
    
    def close(self):
        self.is_visible = False
    

    def handle_event(self, event, base, player, upg, mission, cantor, gold_shop):
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
                self.base_state = 'cantor'
            elif event.key == pygame.K_v:
                self.base_state = 'gold_shop'
                self.gold_selected_idx = 0
            
            if event.key == pygame.K_d and self.base_state == 'storage':
                moved = base.deposit_all(player.inventory)
                for item_id, qty in moved.items():
                    if qty > 0:
                        mission.on_item_depo(item_id, qty)

            if event.key == pygame.K_b and self.base_state == 'upgrade':
                upg.try_upgrade('backpack')

            if event.key == pygame.K_m and self.base_state == 'upgrade':
                upg.try_upgrade('mining')

            if self.base_state == 'gold_shop':
                items = list(gold_shop.upgrades.items())
                if not items:
                    return

                if self.gold_selected_idx >= len(items):
                    self.gold_selected_idx = len(items) - 1
                if self.gold_selected_idx < 0:
                    self.gold_selected_idx = 0

                if event.key == pygame.K_DOWN:
                    self.gold_selected_idx = (self.gold_selected_idx + 1) % len(items)

                elif event.key == pygame.K_UP:
                    self.gold_selected_idx = (self.gold_selected_idx - 1) % len(items)

                elif event.key == pygame.K_RETURN:
                    upg_id, data = items[self.gold_selected_idx]
                    gold_shop.buy_upgrade(upg_id, player)
                    self.gold_msg = f"Bought: {data.get('title', upg_id)}"
                    self.gold_msg_until = pygame.time.get_ticks() + 1200

            if self.base_state == 'cantor' and self.cantor_item_qty == False:
                if event.key == pygame.K_RIGHT:
                    self.cantor_selected_item += 1
                if event.key == pygame.K_LEFT and self.cantor_selected_item >=1:
                    self.cantor_selected_item -= 1
                if event.key == pygame.K_DOWN:
                    self.cantor_selected_item += 5
                if event.key == pygame.K_UP and self.cantor_selected_item >= 5:
                    self.cantor_selected_item -= 5

                if event.key == pygame.K_SPACE:
                    slot = base.storage.slots[self.cantor_selected_item]
                    if slot is None:
                        return  # albo po prostu nic nie rób
                    self.cantor_item_qty = True
                    self.cantor_item_id = slot.item_id
                    self.cantor_qty = 1
            if event.key == pygame.K_ESCAPE and self.base_state == 'cantor':
                self.cantor_item_qty = False
                
            if self.cantor_item_qty:
                if event.key == pygame.K_RIGHT:
                    self.cantor_qty += 1
                elif event.key == pygame.K_LEFT:
                    self.cantor_qty -= 1
                elif event.key == pygame.K_UP:
                    self.cantor_qty += 5
                
            max_have = base.storage.count(self.cantor_item_id)
            if self.cantor_qty > max_have:
                self.cantor_qty = max_have
                
            if self.cantor_item_qty and event.key == pygame.K_RETURN:
                sold, earned = cantor.sell(base.storage, self.cantor_item_id, self.cantor_qty, player)
                self.cantor_item_qty = False
                self.cantor_item_id = None
                self.cantor_qty = 1

                        
                    

        
    def draw(self,invui,base,player, screen : pygame.Surface, upgrade_sys, missions, shop):
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

        if self.base_state == 'cantor':
            screen.blit(self.base_cantor_img,(self.x,self.y))
            storage_rects = invui.draw(screen,base.storage,self.x + 500 ,self.y + 120 , 5, return_rect = True)
            if storage_rects:
                idx = self.cantor_selected_item
                if 0 <= idx < len(storage_rects):
                    pygame.draw.rect(screen, (255, 255, 0), storage_rects[idx], 3, border_radius=6)
            self.draw_cantor_hints(base,self.items,screen)

        if self.base_state == 'gold_shop':
            screen.blit(self.base_cantor_img,(self.x,self.y))
            self.draw_gold_shop(screen, shop.upgrades,player)



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

    
    def draw_missions(self, screen, missions):
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
                
                p = int(prog)
                t = int(target)

                text = f"{title}: {p}/{t}"

            surf = self.font.render(text, True, color)
            screen.blit(surf, (x, y))
            y += line_h

    def draw_gold_shop(self, screen: pygame.Surface, shop: dict, player):
        x0 = self.x + 90
        y0 = self.y + 140
        line_h = 34

        col_left_w = 360
        col_right_w = 50  
        gap = 30

        # headers
        screen.blit(self.font.render("Upgrade", True, self.col_white), (x0, y0))
        screen.blit(self.font.render("Price", True, self.col_white), (x0 + col_left_w + gap, y0))
        y = y0 + line_h

        
        items = list(shop.items())
        row_w = col_left_w + gap + col_right_w
        for i, (upg_id, data) in enumerate(items):
            title = data.get("title", upg_id)
            price = data.get("price", 0)

            can_buy = getattr(player, "gold", 0) >= price
            color = self.col_ok if can_buy else self.col_no

            left_surf = self.font.render(title, True, color)
            screen.blit(left_surf, (x0, y))

            price_txt = f"{int(price)}g"
            right_surf = self.font.render(price_txt, True, color)
            right_x = x0 + col_left_w + gap + col_right_w - right_surf.get_width()
            screen.blit(right_surf, (right_x, y))
            if i == self.gold_selected_idx:
                hi = pygame.Surface((row_w + 16, line_h), pygame.SRCALPHA)
                hi.fill((255, 255, 255, 20))
                screen.blit(hi, (x0 - 8, y - 4))
                pygame.draw.rect(screen, (255, 255, 0), (x0 - 8, y - 4, row_w + 16, line_h), 2, border_radius=6)

            y += line_h

        hint = "UP/DOWN to select   ENTER to buy"
        hint_surf = self.font.render(hint, True, self.col_hint_dim)

        hx = self.x + 70
        hy = self.y + self.panel_h - 60  
        screen.blit(hint_surf, (hx, hy))



            

    def draw_cantor_hints(self, base, ITEMS, screen ,):
        hx = self.x + 70
        hy = self.y + 260
        lh = 22

        lines = []

        if not self.cantor_item_qty:
            lines.append(("cantor", self.col_hint))
            lines.append(("Select slot: Arrow keys", self.col_hint))
            lines.append(("Accept slot: SPACE", self.col_hint))
            lines.append(("Sell: ENTER (after choosing qty)", self.col_hint_dim))
        else:
            lines.append(("cantor", self.col_hint))
            lines.append(("Select qty: LEFT / RIGHT", self.col_hint))
            lines.append(("Sell: ENTER", self.col_hint))
            lines.append(("Cancel: ESC", self.col_hint_dim))

        
        profit_line = None
        if self.cantor_item_id:
            
            have = base.storage.count(self.cantor_item_id)
            qty = max(1, min(self.cantor_qty, have))

            
            price = ITEMS[self.cantor_item_id]["value"] 
            earned = qty * price

            profit_line = f"Selected: {self.cantor_item_id} | Qty: {qty} | Earn: {earned}g"

        for i, (txt, col) in enumerate(lines):
            screen.blit(self.font.render(txt, True, col), (hx, hy + i * lh))

        if profit_line:
            screen.blit(self.font.render(profit_line, True, self.col_hint), (hx, hy + len(lines) * lh + 6))
