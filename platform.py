import pygame
from pygame.locals import *
from entities import *

class Platform(Entity):
    def __init__(self, x, y):
    	"""Handles the creation and images of platforms; they are the P in level creation."""
        Entity.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("images/brick.png"), (22, 20))
        self.rect = Rect(x, y, 13, 20)
        self.mask = pygame.mask.from_surface(self.image)