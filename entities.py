import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self):
    	"""Entities are what the game actually displays on the screen.  Everything created in the game is passed to the entity group during loading."""
        pygame.sprite.Sprite.__init__(self)