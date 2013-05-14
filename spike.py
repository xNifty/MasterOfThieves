import pygame
from pygame.locals import *
from entities import *

class Spike(Entity):
    def __init__(self, x, y):
    	"""Handles the creation and images of spikes in the game class; they are the A in level creation."""
        Entity.__init__(self)
        spike = pygame.transform.scale(pygame.image.load("images/spike.png"), (22, 32))
        self.image = spike.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(x, y, 23, 32)