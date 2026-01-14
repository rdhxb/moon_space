import pygame

class PlayerUI:
    def __init__(self):
        self.text_color = (235, 235, 235)
        self.bg_color = (0, 0, 0, 150)
        self.border_color = (255, 255, 255, 40)

        self.pad = 10
        self.margin = 16
        self.radius = 8  

        self.bar_h = 10
        self.bar_w = 140
        self.bar_gap = 8  # odstęp od tekstu
        self.bar_bg = (255, 255, 255, 25)
        self.bar_fill = (80, 200, 120, 220)
        self.bar_border = (255, 255, 255, 60)

    def draw_player_current_stats(self, screen: pygame.Surface, font: pygame.font.Font, player):
        lvl_txt = f"{int(player.lvl)}"

        fuel_max = getattr(player, "max_fuel", 1)
        fuel = getattr(player, "fuel", 0)
        fuel_pct = 0 if fuel_max <= 0 else max(0.0, min(1.0, fuel / fuel_max))
        fuel_pct_txt = int(fuel_pct * 100)

        lines = [
            f"Lvl: {lvl_txt}",
            f"Backpack: {player.backpack_lvl}",
            f"Mining: {player.mining_lvl}",
            f"Gold: {player.gold}",
        ]

        rendered = [font.render(t, True, self.text_color) for t in lines]
        line_h = font.get_linesize()
        text_w = max(s.get_width() for s in rendered)
        text_h = line_h * len(rendered)

        # panel musi uwzględniać pasek paliwa pod tekstem
        panel_w = max(text_w + self.pad * 2, self.bar_w + self.pad * 2)
        panel_h = text_h + self.pad * 2 + self.bar_gap + self.bar_h

        sw, sh = screen.get_size()
        x = sw - self.margin - panel_w
        y = sh - self.margin - panel_h

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, self.bg_color, (0, 0, panel_w, panel_h), border_radius=self.radius)
        pygame.draw.rect(panel, self.border_color, (0, 0, panel_w, panel_h), width=1, border_radius=self.radius)

        # tekst wyrównany do prawej
        for i, surf in enumerate(rendered):
            tx = panel_w - self.pad - surf.get_width()
            ty = self.pad + i * line_h
            panel.blit(surf, (tx, ty))

        # pasek paliwa (pod tekstem)
        bar_x = panel_w - self.pad - self.bar_w  # też do prawej
        bar_y = self.pad + text_h + self.bar_gap

        # tło paska
        pygame.draw.rect(panel, self.bar_bg, (bar_x, bar_y, self.bar_w, self.bar_h), border_radius=4)

        # wypełnienie wg procentu
        fill_w = int(self.bar_w * fuel_pct)
        if fill_w > 0:
            pygame.draw.rect(panel, self.bar_fill, (bar_x, bar_y, fill_w, self.bar_h), border_radius=4)

        # obramowanie
        pygame.draw.rect(panel, self.bar_border, (bar_x, bar_y, self.bar_w, self.bar_h), width=1, border_radius=4)

        screen.blit(panel, (x, y))
