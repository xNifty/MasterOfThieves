import pygame
from pygame.locals import *
from entities import *

class Door(Entity):
    def __init__(self, x, y):
    	"""Handles the door image and position of the door; it is created with the T and B in level creation."""
        Entity.__init__(self)
        self.closed = True
        door1 = pygame.transform.scale(pygame.image.load("images/door_closed.png"), (32,32))
        self.image = door1.convert_alpha()
        self.rect = Rect(x, y, 32, 5)