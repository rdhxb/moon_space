class HUD:
    def __init__(self, renderer, font):
        self.renderer = renderer
        self.font = font

    def draw(self, screen, game_state, near_base):
        if not near_base:
            return

        if game_state == "play":
            msg = "Naciśnij E, aby wejść do bazy"
        elif game_state == "base_menu":
            msg = "Naciśnij E, aby wyjść"
        else:
            return

        self.renderer.draw_base_hint(screen, self.font, msg)
