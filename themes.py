import pygame
from pygame.locals import *

class Themes():

	def __init__(self, level):
		"""Handles loading the theme for each level by being passed the current level when called within the game class."""
		self.level = level
		self.theme  = pygame.mixer.music.load('sounds/themes/theme' + str(self.level) +'.ogg')