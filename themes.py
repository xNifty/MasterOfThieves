import pygame
from pygame.locals import *
from directory import Directory

class Themes():

	def __init__(self, level):
		"""Handles loading the theme for each level by being passed the current level when called within the game class."""
		self.level = level
		self.theme  = pygame.mixer.music.load(Directory().getDirectory() + '/sounds/themes/theme' + str(self.level) +'.ogg')