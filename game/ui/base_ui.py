# base overlay ui with mission upgrade system inventory ect. i was wondering about bliting an img and then using bous to navigate and i think its a good idea class
import pygame
from ..data.items import ITEMS
class BaseUI():
    def __init__(self, screen_w, screen_h):
        self.home_title = "base"
        self.home_menu = [
            ("[p] storage",   "deposit items"),
            ("[u] upgrade",   "buy backpack / mining upgrades"),
            ("[q] missions",  "show progress"),
            ("[s] cantor",    "sell items for gold"),
            ("[v] gold shop", "buy gold upgrades"),
            ("[e] close",     "close / return"),
        ]
        # Opisy per ekran: 1–2 linie, bez ramek
        self.state_title = {
            "storage": "storage",
            "upgrade": "upgrade",
            "missions": "missions",
            "cantor": "cantor",
            "gold_shop": "gold shop",
        }

        self.state_help_lines = {
            "storage": [
                "[d] deposit all items   [e] return",
                "deposit items from inventory into base storage",
            ],
            "upgrade": [
                "[b] buy backpack upgrade   [m] buy mining upgrade   [e] exit",
                "spend stored materials to upgrade backpack and mining level U have to had min same lvl as upg",
            ],
            "missions": [
                "[e] exit",
                "check mission progress and completion status",
            ],
            "cantor": [
                "select slot: arrows   accept slot: space   sell: enter   cancel: esc",
                "sell items from storage to earn gold",
            ],
            "gold_shop": [
                "select: up/down   buy: enter   [e] return",
                "buy special upgrades using gold",
            ],
        }


        self.base_bg = pygame.image.load('game/data/assets/base/base_bg.png').convert_alpha()

        self.deafult_img_size = (900,600)
        self.base_bg = pygame.transform.smoothscale(self.base_bg,self.deafult_img_size)
        self.base_bg = self.round_corners(self.base_bg,24)


        self.panel_w = 900
        self.panel_h = 600


        self.x, self.y = (screen_w - self.panel_w) // 2, (screen_h - self.panel_h) // 2 

        self.base_state = 'home'
        self.is_visible = False

        # przycimnienie tla 
        self.dim = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        self.dim.fill((0,0,0,140))

        self.font = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
        self.font_title = pygame.font.SysFont("Comic Sans MS", 48, bold=True)
        self.font_menu  = pygame.font.SysFont("Comic Sans MS", 34, bold=True)
        self.font_small = pygame.font.SysFont("Comic Sans MS", 24, bold=True)

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
        self.cantor_item_qty = False
        self.cantor_item_id = None

        self.items = ITEMS

        self.gold_selected_idx = 0



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
            screen.blit(self.base_bg, (self.x, self.y))
            self.draw_home(screen)

        if self.base_state == 'storage':
            screen.blit(self.base_bg,(self.x,self.y))
            self.draw_state_help(screen)

            invui.draw(screen,player.inventory,550,340 , 5)
            invui.draw(screen,base.storage,1000 ,340, 5)



        if self.base_state == 'missions':
            screen.blit(self.base_bg,(self.x,self.y))
            self.draw_missions(screen, missions)
            self.draw_state_help(screen)


        if self.base_state == 'cantor':
            screen.blit(self.base_bg,(self.x,self.y))
            self.draw_state_help(screen, base=base)

            storage_rects = invui.draw(screen,base.storage,1000 ,340 , 5, return_rect = True)
            if storage_rects:
                idx = self.cantor_selected_item
                if 0 <= idx < len(storage_rects):
                    pygame.draw.rect(screen, (255, 255, 0), storage_rects[idx], 3, border_radius=6)

        if self.base_state == 'gold_shop':
            screen.blit(self.base_bg,(self.x,self.y))
            self.draw_gold_shop(screen, shop.upgrades,player)
            self.draw_state_help(screen)





        if self.base_state == 'upgrade':
            screen.blit(self.base_bg, (self.x, self.y))
            self.draw_state_help(screen)


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

    # to round base_bg
    def round_corners(self, surf, radius):
        w, h = surf.get_size()

        # maska: białe (255) = widoczne, przezroczyste = ucięte
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=radius)

        out = surf.copy().convert_alpha()
        out.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return out

    # draw home text
    def draw_home(self, screen):
        title_s = self.font_title.render(self.home_title, True, self.col_white)
        self._blit_center_x(screen, title_s, self.y + 35)

        start_y = self.y + 150
        line_h = 48
        for i, (label, _desc) in enumerate(self.home_menu):
            s = self.font_menu.render(f'{label}: {_desc}', True, self.col_hint)
            self._blit_center_x(screen, s, start_y + i * line_h)
    

    # blit on the center 
    def _blit_center_x(self, screen, surf, y):
        cx = self.x + self.panel_w // 2
        screen.blit(surf, (cx - surf.get_width() // 2, y))

    # draw footer with info how to use fe deposit
    def _draw_footer_lines(self, screen, lines, pad_left=60, pad_bottom=70):
        # 1–2 linie na dole po LEWEJ, bez ramek
        x = self.x + pad_left
        y = self.y + self.panel_h - pad_bottom
        for i, txt in enumerate(lines[:2]):
            surf = self.font_small.render(txt, True, self.col_hint_dim)
            screen.blit(surf, (x, y + i * 22))


    # draw title
    def draw_state_help(self, screen, base=None):
        title = self.state_title.get(self.base_state, self.base_state)
        title_s = self.font_title.render(title, True, self.col_white)
        self._blit_center_x(screen, title_s, self.y + 35)

        lines = self.state_help_lines.get(self.base_state)
        if not lines:
            return

        # Cantor: druga linia dynamiczna (ile dostanie)
        if self.base_state == "cantor" and base is not None:
            lines = [
                lines[0],
                self._cantor_earn_line(base),
            ]

        self._draw_footer_lines(screen, lines)


    # draw how mutch u will earn after selling
    def _cantor_earn_line(self, base):
        if not self.cantor_item_id:
            return "earn: -"

        have = base.storage.count(self.cantor_item_id)
        if have <= 0:
            return "earn: -"

        qty = self.cantor_qty if self.cantor_item_qty else 1
        qty = max(1, min(qty, have))

        price = self.items.get(self.cantor_item_id, {}).get("value", 0)
        earned = int(qty * price)
        return f"selected: {self.cantor_item_id}  qty: {qty}/{have}  earn: {earned}g"

