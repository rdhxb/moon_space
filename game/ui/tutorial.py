import pygame

class Tutorial:
    def __init__(self, screen_w, screen_h):
        self.panel_w = 900
        self.panel_h = 600

        self.tutorial_img = pygame.image.load('game/data/assets/base/base_bg.png').convert_alpha()
        self.deafult_img_size = (900,600)
        self.tutorial_img = pygame.transform.smoothscale(self.tutorial_img,self.deafult_img_size)
        self.tutorial_img = self.round_corners(self.tutorial_img,24)

        self.x = (screen_w - self.panel_w) // 2
        self.y = (screen_h - self.panel_h) // 2

        self.font = pygame.font.SysFont("Comic Sans MS", 20)
        self.font_color = (240, 240, 240)

        self.pad_x = 60
        self.pad_y = 40
        self.line_gap = 6

        self.lines_by_planet = {
            "moon": [
                "Goal:",
                "Explore, mine resources, return to the Base, and upgrade to progress faster.",
                "",
                "Core loop:",
                "1) Explore and find ore.",
                "2) Mine ore and manage your inventory.",
                "3) Watch your fuel while traveling.",
                "4) Return to Base to deposit items, sell for gold, and upgrade.",
                "",
                "Fuel:",
                "- Fuel is consumed while traveling/exploring.",
                "- Fuel is restored when you return to the Base.",
                "",
                "Moon:",
                "- Lower risk, good for early resources.",
                "",
                "Controls:",
                "WASD - Move",
                "E    - Interact / Close panels",
                "I    - Inventory",
                "T    - Open/Close Tutorial",
                "",
                "You can save load game by pressing esc button and the enter"
                "",
                "To go to the nex planet u had to do 5 quests"
            ],
            "mars": [
                "Goal:",
                "Explore Mars, mine resources, return to the Base, and upgrade to handle tougher terrain.",
                "",
                "Core loop:",
                "1) Explore and find ore.",
                "2) Mine ore and manage your inventory.",
                "3) Watch your fuel while traveling.",
                "4) Return to Base to refuel, deposit items, sell for gold, and upgrade.",
                "",
                "Fuel:",
                "- Fuel is consumed while traveling/exploring.",
                "- Fuel is restored when you return to the Base.",
                "",
                "Mars:",
                "- More obstacles and richer nodes (be prepared).",
                "",
                "Controls:",
                "WASD - Move",
                "E    - Interact / Close panels",
                "I    - Inventory",
                "T    - Open/Close Tutorial",
                "",
                "You can save load game by pressing esc button and the enter"
            ],
        }

        self.default_planet_id = "moon"


        self.is_visible = True

    def draw(self, screen: pygame.Surface, planet_id = None):
        if not self.is_visible:
            return
        
        pid = (planet_id or self.default_planet_id)
        pid = str(pid).lower()

        lines = self.lines_by_planet.get(pid, self.lines_by_planet[self.default_planet_id])


        # panel
        screen.blit(self.tutorial_img, (self.x, self.y))

        # tekst w granicach panelu
        text_x = self.x + self.pad_x
        text_y = self.y + self.pad_y

        line_h = self.font.get_linesize() + self.line_gap
        max_lines = (self.panel_h - self.pad_y) // line_h

        for i, line in enumerate(lines[:max_lines]):
            surf = self.font.render(line, True, self.font_color)
            screen.blit(surf, (text_x, text_y + i * line_h))


    def round_corners(self, surf, radius):
        w, h = surf.get_size()

        # maska: białe (255) = widoczne, przezroczyste = ucięte
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=radius)

        out = surf.copy().convert_alpha()
        out.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return out