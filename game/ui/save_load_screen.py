import pygame

class SaveLoadScreen:
    def __init__(self, screen_w: int, screen_h: int, title: str = "SAVE / LOAD"):
        self.w = screen_w
        self.h = screen_h

        self.title = title

        self.options = [
            ("save_game", "Save Game"),
            ("load_game", "Load Game"),
            ("back",      "Back"),
        ]
        self.selected = 0
        self.visible = True

        self.font_title = pygame.font.SysFont("Comic Sans MS", 72, bold=True)
        self.font_item  = pygame.font.SysFont("Comic Sans MS", 44, bold=True)
        self.font_hint  = pygame.font.SysFont("Comic Sans MS", 22, bold=True)

        self.col_bg = (0, 0, 0)
        self.col_text = (235, 235, 235)
        self.col_dim = (170, 170, 170)
        self.col_sel = (255, 255, 0)

    def reset(self):
        self.selected = 0
        self.visible = True

    def handle_event(self, event) -> str | None:
        if not self.visible:
            return None

        if event.type != pygame.KEYDOWN:
            return None

        if event.key == pygame.K_ESCAPE:
            return "back"

        if event.key == pygame.K_UP:
            self.selected = (self.selected - 1) % len(self.options)
            return None

        if event.key == pygame.K_DOWN:
            self.selected = (self.selected + 1) % len(self.options)
            return None

        if event.key == pygame.K_RETURN:
            action, _label = self.options[self.selected]
            return action

        return None

    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return

        screen.fill(self.col_bg)

        # title
        title_surf = self.font_title.render(self.title, True, self.col_text)
        title_x = (self.w - title_surf.get_width()) // 2
        title_y = int(self.h * 0.22)
        screen.blit(title_surf, (title_x, title_y))

        # menu
        start_y = int(self.h * 0.45)
        line_h = 72

        for i, (_action, label) in enumerate(self.options):
            is_sel = (i == self.selected)
            color = self.col_sel if is_sel else self.col_text
            text_surf = self.font_item.render(label, True, color)

            x = (self.w - text_surf.get_width()) // 2
            y = start_y + i * line_h

            if is_sel:
                pad_x, pad_y = 22, 12
                rect = pygame.Rect(
                    x - pad_x, y - pad_y,
                    text_surf.get_width() + pad_x * 2,
                    text_surf.get_height() + pad_y * 2
                )
                hi = pygame.Surface(rect.size, pygame.SRCALPHA)
                hi.fill((255, 255, 255, 18))
                screen.blit(hi, rect.topleft)
                pygame.draw.rect(screen, self.col_sel, rect, 2, border_radius=10)

            screen.blit(text_surf, (x, y))

        hint = "UP/DOWN - select   ENTER - confirm   ESC - back"
        hint_surf = self.font_hint.render(hint, True, self.col_dim)
        hx = (self.w - hint_surf.get_width()) // 2
        hy = int(self.h * 0.88)
        screen.blit(hint_surf, (hx, hy))
