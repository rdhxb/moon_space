import pygame
class IsoRender():
    def __init__(self, world, camera, tile_set):
        self.world = world
        self.camera = camera
        self.tile_set = tile_set

        self.tile_w = 32
        self.tile_h = 16
        self.base_pos = self.world.base_pos

        base_original = self.tile_set.base_img
        bw, bh = base_original.get_size()
        scale = 0.2
        bw2 = int(bw * scale)
        bh2 = int(bh * scale)
        self.base_img_small = pygame.transform.smoothscale(base_original, (bw2, bh2))
        self.base_rect_small = self.base_img_small.get_rect()

        self.base_screen_pos = None


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


    def draw_base(self, screen: pygame.Surface):
        screen_w, screen_h = screen.get_size()
        cx, cy = screen_w // 2, screen_h // 2
        z = self.camera.zoom

        tx, ty = self.world.base_pos

        sx, sy = self.tile_to_screen(tx, ty)

        # 3) zoom pozycji wokół środka ekranu 
        sxz = cx + (sx - cx) * z
        syz = cy + (sy - cy) * z

        # 4) pivot sprite'a w pikselach
        base_img = self.base_img_small
        bw, bh = base_img.get_size()

        pivot_x = bw / 2
        pivot_y = bh - self.tile_h   

        
        if z != 1.0:
            draw_w = int(bw * z)
            draw_h = int(bh * z)
            img = pygame.transform.smoothscale(base_img, (draw_w, draw_h))
            pivot_xz = pivot_x * z
            pivot_yz = pivot_y * z
        else:
            img = base_img
            pivot_xz = pivot_x
            pivot_yz = pivot_y

        
        draw_x = sxz - pivot_xz
        draw_y = syz - pivot_yz

        screen.blit(img, (draw_x, draw_y))

        
        self.base_screen_pos = (sxz, syz)
        self.base_draw_rect = pygame.Rect(draw_x, draw_y, img.get_width(), img.get_height())

        


    def draw_base_hint(self, screen, font, text):
        if not hasattr(self, "base_draw_rect") or self.base_draw_rect is None:
            return

        r = self.base_draw_rect

        # tekst
        surf = font.render(text, True, (255, 255, 255))

        # pozycja: środek nad bazą
        margin = 8
        x = int(r.centerx - surf.get_width() / 2)
        y = int(r.top - surf.get_height() - margin)

        # clamp do ekranu (żeby nie ucinało przy krawędziach)
        sw, sh = screen.get_size()
        x = max(8, min(x, sw - surf.get_width() - 8))
        y = max(8, min(y, sh - surf.get_height() - 8))

        # tło półprzezroczyste
        pad = 8
        bg = pygame.Surface((surf.get_width() + 2*pad, surf.get_height() + 2*pad), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 40))

        screen.blit(bg, (x - pad, y - pad))
        screen.blit(surf, (x, y))
