import pygame
class Camera():
    def __init__(self):
        self.camera_speed = 1
        self.zoom = 2

    
    def move(self, dx, dy):
        self.offset_x += dx
        self.offset_y += dy

    def center_on(self,iso_x,iso_y,screen_w,screen_h):
        self.offset_x = screen_w / 2 - iso_x
        self.offset_y = screen_h / 2 - iso_y



