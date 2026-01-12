import pygame

class Tutorial:
    def __init__(self, screen_w, screen_h):
        self.panel_w = 900
        self.panel_h = 600

        self.tutorial_img = pygame.image.load('game/data/assets/tutorial.png').convert_alpha()
        self.x = (screen_w - self.panel_w) // 2
        self.y = (screen_h - self.panel_h) // 2

        self.font = pygame.font.SysFont("Comic Sans MS", 20)
        self.font_color = (240, 240, 240)

        self.pad_x = 60
        self.pad_y = 120
        self.line_gap = 6

        # Prosty tekst jako linie (bez wrappera)
        self.lines = [
            "Goal:",
            "Collect resources, bring them to the Base, upgrade your ship, and grow stronger.",
            "",
            "Core loop:",
            "1) Explore the surface and find ore.",
            "2) Mine ore and manage your inventory.",
            "3) Return to Base and deposit items to Storage.",
            "4) Sell resources for Gold.",
            "5) Upgrade Backpack and Mining to progress faster.",
            "6) Complete missions to increase your level.",
            "",
            "Controls:",
            "WASD - Move",
            "E    - Interact (Base / Ore)",
            "I    - Inventory",
            "Base: P Storage | U Upgrade | Q Missions | S Shop",
            "Shop: Arrows (select) -> SPACE (choose) -> Arrows (qty) -> ENTER (sell)",
            "T  - Close panels or open Tutorial ",
        ]

        self.is_visible = True

    def draw(self, screen: pygame.Surface):
        if not self.is_visible:
            return

        # panel
        screen.blit(self.tutorial_img, (self.x, self.y))

        # tekst w granicach panelu
        text_x = self.x + self.pad_x
        text_y = self.y + self.pad_y

        line_h = self.font.get_linesize() + self.line_gap
        max_lines = (self.panel_h - self.pad_y) // line_h

        for i, line in enumerate(self.lines[:max_lines]):
            surf = self.font.render(line, True, self.font_color)
            screen.blit(surf, (text_x, text_y + i * line_h))
