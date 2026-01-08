import pygame
class IsoRender():
    def __init__(self, world, camera, tile_set):
        self.world = world
        self.camera = camera
        self.tile_set = tile_set

        self.tile_w = 32
        self.tile_h = 16
        self.base_pos = (10, 10) 

        base_original = self.tile_set.base_img
        bw, bh = base_original.get_size()
        scale = 0.5
        bw2 = int(bw * scale)
        bh2 = int(bh * scale)
        self.base_img_small = pygame.transform.smoothscale(base_original, (bw2, bh2))
        self.base_rect_small = self.base_img_small.get_rect()


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

        screen_w, screen_h = screen.get_size()
        cx, cy = screen_w // 2, screen_h // 2 
        zoom = self.camera.zoom

        for ty in range(h):
            for tx in range(w):
                # 0 = floor, 1 = wall itd.
                tile_id = self.world.get_tile(tx, ty)
                surface_tile = self.tile_set.get_surface(tile_id)
                if surface_tile is None:
                    continue  # brak kafla dla tego ID

                sx, sy = self.tile_to_screen(tx, ty)

                # przesuniecie wzgledem srodka ekranu 
                dx = sx - cx
                dy = sy - cy

                # skalowanie odleglosci od srodka
                sx_zoom = cx + dx * zoom
                sy_zoom = cy  + dy * zoom

                # 4. skalowanie sprite'a kafla
                if zoom != 1.0:
                    tw = int(surface_tile.get_width() * zoom)
                    th = int(surface_tile.get_height() * zoom)
                    if tw <= 0 or th <= 0:
                        continue  # przy ekstremalnie małym zoomie
                    tile_to_draw = pygame.transform.scale(surface_tile, (tw, th))
                else:
                    tile_to_draw = surface_tile

                screen.blit(tile_to_draw, (sx_zoom, sy_zoom))

            
        # trees
    def draw_trees(self,screen: pygame.Surface):
        screen_w, screen_h = screen.get_size()
        cx, cy = screen_w // 2, screen_h // 2 
        zoom = self.camera.zoom

        for (tx, ty) in self.world.trees:
            sx, sy = self.tile_to_screen(tx, ty) 

            tree_img = self.tile_set.tree_image
            tree_w = self.tile_set.tree_rect.width
            tree_h = self.tile_set.tree_rect.height

            # przesunięcie względem środka ekranu
            dx = sx - cx
            dy = sy - cy

            # skalowanie odległości od środka 
            sx_zoom = cx + dx * zoom
            sy_zoom = cy + dy * zoom

            # skalowanie
            if zoom != 1.0:
                tw = int(tree_w * zoom)
                th = int(tree_h * zoom)
                if tw <= 0 or th <= 0:
                    continue

                tile_to_draw = pygame.transform.scale(tree_img, (tw, th))

                # offset drzewa po zoomie
                offset_x = (tree_w // 2) * zoom
                offset_y = (tree_h - self.tile_h) * zoom
            else:
                tile_to_draw = tree_img
                offset_x = tree_w // 2
                offset_y = (tree_h - self.tile_h)

            draw_x = sx_zoom - offset_x
            draw_y = sy_zoom - offset_y

            screen.blit(tile_to_draw, (draw_x, draw_y))


    def draw_base(self,screen: pygame.Surface):
        screen_w, screen_h = screen.get_size()
        cx, cy = screen_w // 2, screen_h // 2 
        zoom = self.camera.zoom
        self.base_pos = (28, 25)
        tx ,ty = self.base_pos
        sx, sy = self.tile_to_screen(tx, ty) 

        base_img = self.base_img_small
        base_w = self.base_rect_small.width
        base_h = self.base_rect_small.height

        # przesunięcie względem środka ekranu
        dx = sx - cx
        dy = sy - cy

        # skalowanie odległości od środka 
        sx_zoom = cx + dx * zoom
        sy_zoom = cy + dy * zoom
        tile_to_draw = pygame.transform.scale(base_img, (base_w, base_h))
        offset_x = (base_w // 2) * zoom
        offset_y = (base_h - self.tile_h) * zoom

        draw_x = sx_zoom - offset_x
        draw_y = sy_zoom - offset_y
        
        screen.blit(tile_to_draw, (draw_x, draw_y))
