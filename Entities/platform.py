import pygame
from pygame.locals import *
from BuildFunctions.directory import Directory
from Entities.entities import Entity

class Platform(Entity):
    def __init__(self, x, y):
        """Handles the creation and images of platforms; they are the P in level creation."""
        Entity.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(Directory().get_directory() + "/images/brick.png"), (32, 32))
        self.rect = Rect(x, y, 23, 32)
        self.mask = pygame.mask.from_surface(self.image)