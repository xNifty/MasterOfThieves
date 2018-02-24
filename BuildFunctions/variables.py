import pygame
from pygame.locals import *

class Variables(object):
    volume = 0.0
    canUseKeys = True
    muted = True
    loadedTheme = False
    total_time = 0
    showTime = False
    old_volume = 0.0

    def saveVolume(old):
        oldVolume = volume