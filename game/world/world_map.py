import pygame
from random import choice

class WorldMap():
    def __init__(self):
        self.tile_data = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            
        ]

        self.height_in_tiles = len(self.tile_data)
        self.width_in_tiles = len(self.tile_data[0])
        self.trees = []
        self.base_pos = (15,15)
        self.trees_amount = 4
        self.iron_ores = []
        self.ores_amount = 3



    def get_tile(self, tx, ty):
        # poza mapą = ściana
        if tx < 0 or ty < 0 or tx >= self.width_in_tiles or ty >= self.height_in_tiles:
            return 1

        return self.tile_data[ty][tx]
    
    def create_tree(self):
        self.free_tiles = []

        for ty in range(self.height_in_tiles):
            for tx in range(self.width_in_tiles):
                if self.tile_data[ty][tx] == 0:
                    self.free_tiles.append((tx, ty))

        base_tx, base_ty = self.base_pos
        radius = 5

        filtered_tiles = []
        for (tx, ty) in self.free_tiles:
            dx = tx - base_tx
            dy = ty - base_ty
            if abs(dx) <= radius and abs(dy) <= radius:
                continue
            filtered_tiles.append((tx, ty))

        self.free_tiles = filtered_tiles

        for _ in range(self.trees_amount):
            pos = choice(self.free_tiles)
            self.trees.append(pos)
            self.free_tiles.remove(pos)
            


    def create_iron_ores(self):
        for _ in range(self.ores_amount):
            pos = choice(self.free_tiles)
            self.iron_ores.append(pos)
            self.free_tiles.remove(pos)
                 
            