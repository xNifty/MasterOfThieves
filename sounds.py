import pygame
from pygame.locals import *

class Sounds():

	def __init__(self):
		"""Handles loading the sound files; they are called by doing sounds.NAME in the game class."""
		self.coin_sound = pygame.mixer.Sound('sounds/game/coin_sound.wav')
		self.death_sound = pygame.mixer.Sound('sounds/game/death.wav')
		self.door = pygame.mixer.Sound('sounds/game/door.wav')
		self.volume = 0.05
		self.mute = False

	def getVolume(self):
		return self.volume