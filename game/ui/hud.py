import pygame
class HUD:
    def __init__(self, renderer, font):
        self.renderer = renderer
        self.font = font

    def draw(self, screen, game_state, near_base, planet_manager=None, mission=None):
        if game_state == "play":
            if near_base:
                msg = "Press E To Enter The Base"
                self.renderer.draw_base_hint(screen, self.font, msg)

            self._draw_top_unlock_msg(screen, planet_manager, mission)

        elif game_state == "base_menu":
            if near_base:
                msg = "Press E to leave"
                self.renderer.draw_base_hint(screen, self.font, msg)

    def _draw_top_unlock_msg(self, screen, planet_manager, mission):
        if planet_manager is None or mission is None:
            return

        if planet_manager.is_unlocked("mars"):
            return

        completed = getattr(mission, "compleated_count", 0)
        if not planet_manager.can_unlock("mars", completed):
            return

        msg = "Planet Mars Unlocked - press 1 to teleport"

        surf = self.font.render(msg, True, (255, 255, 0))
        x = (screen.get_width() - surf.get_width()) // 2
        y = 18

        pad_x, pad_y = 14, 8
        bg = pygame.Surface((surf.get_width() + pad_x * 2, surf.get_height() + pad_y * 2), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 160))
        screen.blit(bg, (x - pad_x, y - pad_y))

        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (x - pad_x, y - pad_y, bg.get_width(), bg.get_height()),
            2,
            border_radius=10
        )

        screen.blit(surf, (x, y))
