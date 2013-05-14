import pygame
from pygame.locals import *

WIN_WIDTH = 1600
WIN_HEIGHT = 950
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
CAMERA_SLACK = 30

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
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    #l = min(0, l)                           # stop scrolling at the left edge
    #l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    #t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    #t = min(0, t)                           # stop scrolling at the top
    return Rect(l, t, w, h)