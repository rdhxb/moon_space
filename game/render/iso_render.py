import pygame
from ..world.world_map import WorldMap
from ..render.TileSet import TileSet

class IsoRender():
    def __init__(self):
        self.world = WorldMap()
        self.tile_set = TileSet()

        self.tile_w = 32
        self.tile_h = 16

        self.offset_x, self.offset_y = 1920 // 2, 1080 // 2

    def tile_to_screen(self, tx, ty):
        half_w = self.tile_w //2
        half_h = self.tile_h //2


        sx = (tx - ty) * half_w
        sy = (tx + ty) * half_h

        sx += self.offset_x
        sy += self.offset_y

        return (sx, sy)
        


    def draw_world(self, screen: pygame.Surface):
        h = self.world.height_in_tiles
        w = self.world.width_in_tiles

        for ty in range(h):
            for tx in range(w):
                # 0 = floor, 1 = wall itd.
                tile_id = self.world.get_tile(tx, ty)
                surface_tile = self.tile_set.get_surface(tile_id)
                if surface_tile is None:
                    continue  # brak kafla dla tego ID

                sx, sy = self.tile_to_screen(tx, ty)
                screen.blit(surface_tile, (sx, sy))

