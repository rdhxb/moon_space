import pygame

class PlayerUI:
    def __init__(self):
        self.text_color = (235, 235, 235)
        self.bg_color = (0, 0, 0, 150)
        self.border_color = (255, 255, 255, 40)

        self.pad = 10
        self.margin = 16
        self.radius = 8  

    def draw_player_current_stats(self, screen: pygame.Surface, font: pygame.font.Font, player):
        lvl_txt = f"{int(player.lvl)}"
        lines = [
            f"Lvl: {lvl_txt}",
            f"Backpack: {player.backpack_lvl}",
            f"Mining: {player.mining_lvl}",
            f'Gold: {player.gold}',
        ]

        # render linii, policz wymiary
        rendered = [font.render(t, True, self.text_color) for t in lines]
        line_h = font.get_linesize()
        text_w = max(s.get_width() for s in rendered)
        text_h = line_h * len(rendered)

        panel_w = text_w + self.pad * 2
        panel_h = text_h + self.pad * 2

        sw, sh = screen.get_size()
        x = sw - self.margin - panel_w
        y = sh - self.margin - panel_h

        # panel tła (SRCALPHA, żeby działała przezroczystość)
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, self.bg_color, (0, 0, panel_w, panel_h), border_radius=self.radius)
        pygame.draw.rect(panel, self.border_color, (0, 0, panel_w, panel_h), width=1, border_radius=self.radius)

        # tekst wyrównany do prawej wewnątrz panelu
        for i, surf in enumerate(rendered):
            tx = panel_w - self.pad - surf.get_width()
            ty = self.pad + i * line_h
            panel.blit(surf, (tx, ty))

        screen.blit(panel, (x, y))
