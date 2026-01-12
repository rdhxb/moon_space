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

        self._tile_cache = {}          
        self._cache_zoom_key = None   


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

        sw, sh = screen.get_size()
        cx, cy = sw // 2, sh // 2
        zoom = self.camera.zoom

        tiles_x = int((sw / (self.tile_w * zoom)) * 2) + 8
        tiles_y = int((sh / (self.tile_h * zoom)) * 2) + 8


        center_tx = getattr(self.world, "center_tx", w // 2)
        center_ty = getattr(self.world, "center_ty", h // 2)

        min_tx = max(0, center_tx - tiles_x)
        max_tx = min(w - 1, center_tx + tiles_x)
        min_ty = max(0, center_ty - tiles_y)
        max_ty = min(h - 1, center_ty + tiles_y)

        for ty in range(min_ty, max_ty + 1):
            for tx in range(min_tx, max_tx + 1):
                tile_id = self.world.get_tile(tx, ty)
                tile_to_draw = self._get_tile_surface_cached(tile_id, zoom)
                if tile_to_draw is None:
                    continue

                sx, sy = self.tile_to_screen(tx, ty)

                dx = sx - cx
                dy = sy - cy
                sxz = cx + dx * zoom
                syz = cy + dy * zoom

                screen.blit(tile_to_draw, (sxz, syz))


            
    def draw_sprites_helper(self, screen: pygame.Surface, img_attr: str, rect_attr: str, positions):
        screen_w, screen_h = screen.get_size()
        cx, cy = screen_w // 2, screen_h // 2
        zoom = self.camera.zoom

        img = getattr(self.tile_set, img_attr)      
        rect = getattr(self.tile_set, rect_attr)          
        img_w = rect.width
        img_h = rect.height

        for (tx, ty) in positions:
            sx, sy = self.tile_to_screen(tx, ty)

            dx = sx - cx
            dy = sy - cy
            sx_zoom = cx + dx * zoom
            sy_zoom = cy + dy * zoom

            if zoom != 1.0:
                tw = int(img_w * zoom)
                th = int(img_h * zoom)
                if tw <= 0 or th <= 0:
                    continue
                tile_to_draw = pygame.transform.scale(img, (tw, th))
                offset_x = (img_w / 2) * zoom
                offset_y = (img_h - self.tile_h) * zoom
            else:
                tile_to_draw = img
                offset_x = img_w / 2
                offset_y = (img_h - self.tile_h)

            draw_x = sx_zoom - offset_x
            draw_y = sy_zoom - offset_y
            screen.blit(tile_to_draw, (draw_x, draw_y))


    def draw_base(self, screen: pygame.Surface):
        screen_w, screen_h = screen.get_size()
        cx, cy = screen_w // 2, screen_h // 2
        zoom = self.camera.zoom

        tx, ty = self.world.base_pos

        sx, sy = self.tile_to_screen(tx, ty)

        # 3) zoom pozycji wokół środka ekranu 
        sxz = cx + (sx - cx) * zoom
        syz = cy + (sy - cy) * zoom

        # 4) pivot sprite'a w pikselach
        base_img = self.base_img_small
        bw, bh = base_img.get_size()

        pivot_x = bw / 2
        pivot_y = bh - self.tile_h   

        
        if zoom != 1.0:
            draw_w = int(bw * zoom)
            draw_h = int(bh * zoom)
            img = pygame.transform.smoothscale(base_img, (draw_w, draw_h))
            pivot_xz = pivot_x * zoom
            pivot_yz = pivot_y * zoom
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

    def draw_ore_hint(self,screen: pygame.Surface, font, ore_tile, camera):
        # jesli jest nad ruda czyli game.near_ore = True to blituje napis maly E nad ruda to bedzie do wylaczenie w ustawieniach jak kazdy hint
        # find ore x and y 

        # nizej tylko przeliczanie tx o ty ore bo to mamy na px ekranu zeby dalo sie blitowac pewnie funkcja by sie przydala bo wszsytko ma hinty ale to potem 
        sw, sh = screen.get_size()
        ore_tx , ore_ty = ore_tile
        
        
        sx = (ore_tx - ore_ty) * 16 + camera.offset_x
        sy = (ore_tx + ore_ty) * 8 + camera.offset_y

        cx, cy = sw // 2, sh // 2
        z = camera.zoom

        sxz = cx + (sx - cx) * z
        syz = cy + (sy - cy) * z

        over_ore = 30

        screen.blit(font.render('E',False, "#BF0930CA"), (sxz ,syz - over_ore))


    
    def _get_tile_surface_cached(self, tile_id: int, zoom: float):
        zoom_key = round(zoom, 2)

        if self._cache_zoom_key != zoom_key:
            self._tile_cache.clear()
            self._cache_zoom_key = zoom_key

        key = (tile_id, zoom_key)
        surf = self._tile_cache.get(key)
        if surf is not None:
            return surf

        base = self.tile_set.get_surface(tile_id)
        if base is None:
            return None

        if zoom_key == 1.0:
            surf = base
        else:
            tw = int(base.get_width() * zoom_key)
            th = int(base.get_height() * zoom_key)
            if tw <= 0 or th <= 0:
                return None
            surf = pygame.transform.smoothscale(base, (tw, th))

        self._tile_cache[key] = surf
        return surf





