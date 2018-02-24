import pygame
from pygame.locals import *
from BuildFunctions.directory import Directory
from .entities import Entity

class Coins(Entity):
    def __init__(self, x, y):
        """Handles the coins image and size; they are O in the level creation."""
        Entity.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(Directory().get_directory() + "/images/coin.png"), (22, 20))
        self.mask = pygame.mask.from_surface(self.image)
        self.image.convert_alpha()
        self.rect = Rect(x, y, 22, 20)