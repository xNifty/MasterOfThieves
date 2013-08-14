import pygame
from pygame.locals import *
from entities import *

class Trophy(Entity):

    def __init__(self, x, y, level):
    	"""Handles loading the correct trophy image for each level and it's location based on being passed an X, Y, and the current level within the game class when the level is loaded (it is the X)."""
        Entity.__init__(self)
        self.level = level
        trophy = pygame.transform.scale(pygame.image.load("images/trophies/trophy" + str(self.level) + ".png"), (32, 32))
        self.image = trophy.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(x, y, 32, 32)