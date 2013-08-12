import pygame
from pygame.locals import *

class Display(object):
	def __init__(self):
		self.WIN_WIDTH = 800
		self.WIN_HEIGHT = 500
		self.HALF_WIDTH = int(self.WIN_WIDTH / 2)
		self.HALF_HEIGHT = int(self.WIN_HEIGHT / 2)

		self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
		self.DEPTH = 32
		self.FLAGS = 0
		self.CAMERA_SLACK = 30

	def getWinWidth(self):
		return self.WIN_WIDTH

	def getWinHeight(self):
		return self.WIN_HEIGHT

	def getHalfHeight(self):
		return self.HALF_HEIGHT

	def getHalfWidth(self):
		return self.HALF_WIDTH

	def getDisplay(self):
		return self.DISPLAY

	def getDepth(self):
		return self.DEPTH

	def getFlags(self):
		return self.FLAGS