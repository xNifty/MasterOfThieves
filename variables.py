import pygame
from pygame.locals import *

class Variables(object):
	volume = 0.2
	canUseKeys = True
	muted = False
	loadedTheme = False
	total_time = 0
	showTime = False
	oldVolume = 0.0

	def saveVolume(old):
		oldVolume = volume