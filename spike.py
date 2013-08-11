import pygame
from pygame.locals import *
from entities import *

class Spike(Entity):
    def __init__(self, x, y, number):
    	"""Handles the creation and images of spikes in the game class; A(1) = up, V(2) = down, >(3) = right, <(4) = left"""
        Entity.__init__(self)
        self.number = number
        spike = pygame.transform.scale(pygame.image.load("images/spike" + str(self.number) +".png"), (32, 32))
        self.image = spike.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(x, y, 32, 32)