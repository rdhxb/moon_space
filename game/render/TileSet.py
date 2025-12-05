import pygame 

class TileSet():
    def __init__(self):
        self.tile_width = 32
        self.tile_floor_height = 16
        self.tile_wall_height = 32

        self.file_name_floor = 'game/data/assets/moon_floor.png'
        self.file_name_wall = 'game/data/assets/moon_wall.png'

        self.image_floor = pygame.image.load(self.file_name_floor).convert_alpha()
        self.image_wall = pygame.image.load(self.file_name_wall).convert_alpha()

        self.rect_floor = self.image_floor.get_rect()
        self.rect_wall = self.image_wall.get_rect()

        self.tiles = {
            0: self.image_floor.subsurface(64,0,self.tile_width,self.tile_floor_height),
            1: self.image_wall.subsurface(32,0,self.tile_width,self.tile_wall_height),
        }

    def get_surface(self, tile_id: int) -> pygame.Surface | None:
        return self.tiles.get(tile_id, None)
