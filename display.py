import pygame
from pygame.locals import *
import os
from sys import exit

from directory import Directory

pygame.init()

class Display(object):
	def __init__(self):
		os.environ['SDL_VIDEO_CENTERED'] = '1'

		self.WIN_WIDTH = 800
		self.WIN_HEIGHT = 800
		self.HALF_WIDTH = int(self.WIN_WIDTH / 2)
		self.HALF_HEIGHT = int(self.WIN_HEIGHT / 2)

		self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
		self.DEPTH = 32
		self.FLAGS = 0
		self.CAMERA_SLACK = 30

		self.screen = pygame.display.set_mode(self.DISPLAY, self.FLAGS, self.DEPTH)
		self.screen_rect = self.screen.get_rect()

		self.font = pygame.font.SysFont("arial", 25)

		self.loadingBar = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/button.png"), (self.WIN_WIDTH, 35))

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

	def gameOver(self):
		self.wonGame = self.font.render("You beat Master of Thieves!", True, (255,255,255))
		self.screen.blit(self.loadingBar, (0,0))
		self.screen.blit(self.wonGame, (10,2))

	def loadingLevel(self, level):
		self.level = level
		self.loading = self.font.render("Loading level: " + str(self.level), True, (255,255,255))
		self.screen.blit(self.loadingBar, (0,0))
		self.screen.blit(self.loading, (10,2))

	def titleScreen(self):
		pygame.display.set_caption("Master of Thieves") # Window caption
		self.background_image = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/intro/title_bg.png"), (self.WIN_WIDTH, self.WIN_HEIGHT)) # Load the title background

		# All of the button images - probably should have loaded through images like the rest
		self.play = pygame.image.load(Directory().getDirectory() + '/images/intro/play.png')
		self.play2 = pygame.image.load(Directory().getDirectory() + '/images/intro/play2.png')
		self.exit = pygame.image.load(Directory().getDirectory() + '/images/intro/exit.png')
		self.exit2 = pygame.image.load(Directory().getDirectory() + '/images/intro/exit2.png')
		self.tut = pygame.image.load(Directory().getDirectory() + '/images/intro/tutorial.png')
		self.tut2 = pygame.image.load(Directory().getDirectory() + '/images/intro/tutorial2.png')

		# Blit the initial images to the screen; order: PLAY, TUT, EXIT
		self.screen.blit(self.background_image, (0,0))
		self.b1 = self.screen.blit(self.play, (0, 100))
		self.b2 = self.screen.blit(self.tut, (0, 200))
		self.b3 = self.screen.blit(self.exit, (0, 300))
		self.title = True # Title status is true while the game waits for the user to make a choice

		# We want the cursor on the main menu and tutorial screen.
		pygame.mouse.set_visible(True)
		pygame.display.update()

	def reloadTitleScreen(self):
		self.title = True
		self.titleScreen()
		pygame.display.update()

	def tutorial(self):
		pygame.display.set_caption("Master of Thieves")
		self.background_image = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/intro/tutscreen.png"), (self.WIN_WIDTH, self.WIN_HEIGHT)) # Tutorial background
		self.screen.blit(self.background_image, (0,0))

		# Menu buttons
		self.menu = pygame.image.load(Directory().getDirectory() + '/images/intro/menu.png')
		self.menu2 = pygame.image.load(Directory().getDirectory() + '/images/intro/menu2.png')

		self.m1 = self.screen.blit(self.menu, (0,0))
		self.tutstatus = True
		while self.tutstatus == True:
		    for e in pygame.event.get():
		        self.pos = pygame.mouse.get_pos()
		        if e.type == QUIT: # "X"ed out of the game
		    		exit()
		        if e.type == MOUSEMOTION:
		            if self.m1.collidepoint(self.pos): # Scrolling over the Main Menu button, so change the image so the user knows they are on it
		                self.screen.blit(self.menu2, (0,0))
		            else:
		                self.screen.blit(self.menu, (0,0)) # Change back to the normal image since the user is no longer on it
		        if e.type == MOUSEBUTTONDOWN:
		            if self.m1.collidepoint(self.pos):
		            	self.tutstatus = False
		                self.titleScreen() # Clicked to go back to main menu
		                pygame.display.update()
		    pygame.display.update()