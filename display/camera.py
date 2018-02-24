import pygame
from pygame.locals import *
from .display import Display

Display = Display()

class Camera(object):
    def __init__(self, camera_func, width, height):
        """Handles the camera for the game, keeping in on the player and allowing scrolling; the window size is handled above."""
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def complex_camera(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l + Display.get_half_width(), -t + Display.get_half_height(), w, h

    #l = min(0, l)                           # stop scrolling at the left edge
    #l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    #t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    #t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)