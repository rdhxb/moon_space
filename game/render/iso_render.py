import pygame
class IsoRender():
    def __init__(self, world, camera, tile_set):
        # self.world = WorldMap()
        # self.tile_set = TileSet()
        self.world = world
        self.camera = camera
        self.tile_set = tile_set

        self.tile_w = 32
        self.tile_h = 16

    def tile_to_screen(self, tx, ty):
        half_w = self.tile_w //2
        half_h = self.tile_h //2


        sx = (tx - ty) * half_w
        sy = (tx + ty) * half_h

        sx += self.camera.offset_x
        sy += self.camera.offset_y

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

            
        # print(self.world.trees)
        # trees
        for (tx, ty) in self.world.trees:
            sx, sy = self.tile_to_screen(tx, ty)

            tree_img = self.tile_set.tree_image
            tree_w = self.tile_set.tree_rect.width
            tree_h = self.tile_set.tree_rect.height

            draw_x = sx - tree_w // 2
            draw_y = sy - (tree_h - self.tile_h)

            screen.blit(tree_img, (draw_x, draw_y))

