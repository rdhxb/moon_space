from random import randint, choice
import math

class MarsMap:
    FLOOR = 0
    WALL = 1

    def __init__(self, w=128, h=128, base_pos=(15, 15)):
        self.width_in_tiles = w
        self.height_in_tiles = h
        self.base_pos = base_pos

        self.tile_data = [[self.FLOOR for _ in range(w)] for _ in range(h)]
        for x in range(w):
            self.tile_data[0][x] = self.WALL
            self.tile_data[h-1][x] = self.WALL
        for y in range(h):
            self.tile_data[y][0] = self.WALL
            self.tile_data[y][w-1] = self.WALL

        
        self.objects_by_type = {}    
        self.blocked_tiles = set()   

        self._floor_tiles = [(x, y) for y in range(h) for x in range(w) if self.tile_data[y][x] == self.FLOOR]

        self._generate()

    def get_tile(self, tx, ty):
        if tx < 0 or ty < 0 or tx >= self.width_in_tiles or ty >= self.height_in_tiles:
            return self.WALL
        return self.tile_data[ty][tx]

    def is_blocked(self, tx, ty):
        return (tx, ty) in self.blocked_tiles or self.get_tile(tx, ty) == self.WALL

    def _generate(self):
        bx, by = self.base_pos
        safe_r = 8  

        occupied = set()
        for (tx, ty) in self._floor_tiles:
            if self._dist(tx, ty, bx, by) <= safe_r:
                occupied.add((tx, ty))

        # spawn przeszkód (blokują ruch)
        self._spawn("dust_dune", count=25, min_dist=safe_r+2, occupied=occupied, blocks=True)
        self._spawn("tree_mars", count=120,  min_dist=10,      occupied=occupied, blocks=True)

        self._spawn("red_hematite_ore",   count=140, min_dist=safe_r,   occupied=occupied, blocks=False)
        self._spawn("ferrosilicate_ore", count=90,  min_dist=16,       occupied=occupied, blocks=False)
        self._spawn("sulfide_vein_ore",   count=35,  min_dist=28,       occupied=occupied, blocks=False)

    def _spawn(self, sprite_id, count, min_dist, occupied, blocks: bool):
        if sprite_id not in self.objects_by_type:
            self.objects_by_type[sprite_id] = set()

        bx, by = self.base_pos
        tries = 0
        placed = 0
        max_tries = count * 40

        while placed < count and tries < max_tries:
            tries += 1
            tx, ty = choice(self._floor_tiles)

            if (tx, ty) in occupied:
                continue
            if self._dist(tx, ty, bx, by) < min_dist:
                continue

            self.objects_by_type[sprite_id].add((tx, ty))
            occupied.add((tx, ty))
            placed += 1

            if blocks:
                self.blocked_tiles.add((tx, ty))

    def _dist(self, x1, y1, x2, y2):
        dx = x1 - x2
        dy = y1 - y2
        return math.sqrt(dx*dx + dy*dy)
