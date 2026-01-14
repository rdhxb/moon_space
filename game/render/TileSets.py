import pygame

class BaseTileSet:
    tile_width = 32
    tile_floor_height = 16
    tile_wall_height = 32

    def __init__(self):
        self.tiles: dict[int, pygame.Surface] = {}
        self.sprites: dict[str, pygame.Surface] = {}

        # jeśli wszędzie używasz base_img w IsoRender, trzymaj to wspólnie:
        self.base_img = pygame.image.load("game/data/assets/basee_one.png").convert_alpha()

    def get_surface(self, tile_id: int):
        return self.tiles.get(tile_id)

    def get_sprite(self, sprite_id: str):
        return self.sprites.get(sprite_id)



class MoonTileSet(BaseTileSet):
    def __init__(self):
        super().__init__()

        # tiles
        floor_sheet = pygame.image.load("game/data/assets/moon_floor.png").convert_alpha()
        wall_sheet  = pygame.image.load("game/data/assets/moon_wall.png").convert_alpha()

        self.tiles = {
            0: floor_sheet.subsurface(64, 0, self.tile_width, self.tile_floor_height),
            1: wall_sheet.subsurface(32, 0, self.tile_width, self.tile_wall_height),
        }

        tree = pygame.image.load("game/data/assets/tree.png").convert_alpha()
        ore_iron = pygame.image.load("game/data/assets/iron_ore.png").convert_alpha()  # fallback

        
        self.sprites = {
            "tree": tree,
            "ore_iron": ore_iron,
        }


class MarsTileSet(BaseTileSet):
    def __init__(self):
        super().__init__()

        floor_sheet = pygame.image.load("game/data/assets/moon_floor.png").convert_alpha()
        wall_sheet  = pygame.image.load("game/data/assets/moon_wall.png").convert_alpha()

        self.tiles = {
            0: floor_sheet.subsurface(0, 0, self.tile_width, self.tile_floor_height),
            1: wall_sheet.subsurface(0, 0, self.tile_width, self.tile_wall_height),
        }        

        # przeszskody
        dust_dune = pygame.image.load("game/data/assets/mushroom1_dark_shadow3.png").convert_alpha()
        tree_mars = pygame.image.load("game/data/assets/tree_mars.png").convert_alpha()

        # rudy  
        red_hematite_ore = pygame.image.load("game/data/assets/Red_crystal4.png").convert_alpha()
        ferrosilicate_ore = pygame.image.load("game/data/assets/Violet_crystal4.png").convert_alpha()
        sulfide_vein_ore = pygame.image.load("game/data/assets/Yellow-green_crystal4.png").convert_alpha()

        self.sprites = {
            # rudy
            "red_hematite_ore": red_hematite_ore,
            "ferrosilicate_ore": ferrosilicate_ore,
            "sulfide_vein_ore": sulfide_vein_ore,

            # przeszkody
            "dust_dune": dust_dune,
            "tree_mars": tree_mars,
        }
