import pygame
class Camera():
    def __init__(self):
        self.offset_x = 1920 // 2
        self.offset_y = 1080 // 2

        self.camera_speed = 100

    
    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy



