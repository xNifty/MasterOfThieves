import pygame
from pygame.locals import *
import os
import webbrowser
from sys import exit
import Tkinter
import tkMessageBox

from directory import Directory
from sounds import Sounds
from variables import Variables
from deaths import Deaths

pygame.init()
sounds = Sounds()
deaths = Deaths()
root = Tkinter.Tk()
root.withdraw()

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

		self.GAMENAME = "Master of Thieves"
		self.icon = pygame.image.load(Directory().getDirectory() + "/images/winicon.ico")
		self.icon.set_alpha(0)
		pygame.display.set_icon(self.icon)

		self.screen = pygame.display.set_mode(self.DISPLAY, self.FLAGS, self.DEPTH)
		self.screen_rect = self.screen.get_rect()

		self.font = pygame.font.SysFont("arial", 25)
		self.buildFont = pygame.font.SysFont("arial", 12)

		self.loadingBar = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/button.png"), (self.WIN_WIDTH, 35))

		self.optionsMenu = False

		self.gameVersion = self.buildFont.render('Alpha 2.0.1', True, (0,0,0))

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
		self.wonGame = self.font.render("You beat " + self.GAMENAME + "!", True, (255,255,255))
		self.screen.blit(self.loadingBar, (0,0))
		self.screen.blit(self.wonGame, (10,2))

	def loadingLevel(self, level):
		self.level = level
		self.loading = self.font.render("Loading level: " + str(self.level), True, (255,255,255))
		self.screen.blit(self.loadingBar, (0,0))
		self.screen.blit(self.loading, (10,2))

	def titleScreen(self):
		pygame.display.set_caption(self.GAMENAME) # Window caption
		self.background_image = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/intro/title_bg.png"), (self.WIN_WIDTH, self.WIN_HEIGHT)) # Load the title background

		# All of the button images - probably should have loaded through images like the rest
		self.play = pygame.image.load(Directory().getDirectory() + '/images/intro/play.png')
		self.play2 = pygame.image.load(Directory().getDirectory() + '/images/intro/play2.png')
		self.exit = pygame.image.load(Directory().getDirectory() + '/images/intro/exit.png')
		self.exit2 = pygame.image.load(Directory().getDirectory() + '/images/intro/exit2.png')
		self.tut = pygame.image.load(Directory().getDirectory() + '/images/intro/tutorial.png')
		self.tut2 = pygame.image.load(Directory().getDirectory() + '/images/intro/tutorial2.png')
		self.options = pygame.image.load(Directory().getDirectory() + '/images/intro/options.png')
		self.options2 = pygame.image.load(Directory().getDirectory() + '/images/intro/options1.png')

		# Blit the initial images to the screen; order: PLAY, TUT, EXIT
		self.screen.blit(self.background_image, (0,0))
		self.b1 = self.screen.blit(self.play, (0,100))
		self.b2 = self.screen.blit(self.tut, (0,200))
		self.b3 = self.screen.blit(self.options, (0,300))
		self.b4 = self.screen.blit(self.exit, (0,400))
		self.title = True # Title status is true while the game waits for the user to make a choice

		# We want the cursor on the main menu and tutorial screen.
		pygame.mouse.set_visible(True)
		pygame.display.update()

	def reloadTitleScreen(self):
		self.title = True
		self.titleScreen()
		pygame.display.update()

	def tutorial(self):
		pygame.display.set_caption(self.GAMENAME)
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
		                self.getGameVersion()
		                pygame.display.update()
		    pygame.display.update()

	def getGameVersion(self):
		self.screen.blit(self.gameVersion,  (1, self.WIN_HEIGHT-15))

	def optionsScreen(self):
		self.background_image = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/intro/title_bg.png"), (self.WIN_WIDTH, self.WIN_HEIGHT)) # Tutorial background
		self.screen.blit(self.background_image, (0,0))

		self.menu = pygame.image.load(Directory().getDirectory() + '/images/intro/menu.png')
		self.menu2 = pygame.image.load(Directory().getDirectory() + '/images/intro/menu2.png')
		self.mute = pygame.image.load(Directory().getDirectory() + '/images/intro/mute.png')
		self.mute1 = pygame.image.load(Directory().getDirectory() + '/images/intro/mute1.png')
		self.volumeInc = pygame.image.load(Directory().getDirectory() + '/images/intro/volume+.png')
		self.volumeInc1 = pygame.image.load(Directory().getDirectory() + '/images/intro/volume+1.png')
		self.volumeDec = pygame.image.load(Directory().getDirectory() + '/images/intro/volume-.png')
		self.volumeDec1 = pygame.image.load(Directory().getDirectory() + '/images/intro/volume-1.png')
		self.showTime = pygame.image.load(Directory().getDirectory() + '/images/intro/showtime.png')
		self.showTime1 = pygame.image.load(Directory().getDirectory() + '/images/intro/showtime1.png')
		self.bug = pygame.image.load(Directory().getDirectory() + '/images/intro/bug.png')
		self.bug1 = pygame.image.load(Directory().getDirectory() + '/images/intro/bug1.png')

		self.m1 = self.screen.blit(self.menu, (0,100))
		self.m2 = self.screen.blit(self.mute, (0,200))
		self.m3 = self.screen.blit(self.volumeInc, (0,300))
		self.m4 = self.screen.blit(self.volumeDec, (0,400))
		self.m5 = self.screen.blit(self.showTime, (0,500))
		self.m6 = self.screen.blit(self.bug, (0,600))

		while self.optionsMenu == True:
			pygame.display.set_caption(self.GAMENAME + " - Options | Muted: " + str(Variables.muted) + " | Current Volume: " + str(Variables.volume) + " | time-per-level: " + str(Variables.showTime))
			for e in pygame.event.get():
				self.pos = pygame.mouse.get_pos()
				if e.type == QUIT:
					exit()
				if e.type == MOUSEMOTION:
					if self.m1.collidepoint(self.pos):
						self.screen.blit(self.menu2, (0,100))
					elif self.m2.collidepoint(self.pos):
						self.screen.blit(self.mute1, (0,200))
					elif self.m3.collidepoint(self.pos):
						self.screen.blit(self.volumeInc1, (0,300))
					elif self.m4.collidepoint(self.pos):
						self.screen.blit(self.volumeDec1, (0,400))
					elif self.m5.collidepoint(self.pos):
						self.screen.blit(self.showTime1, (0,500))
					elif self.m6.collidepoint(self.pos):
						self.screen.blit(self.bug1, (0,600))
					else:
						self.screen.blit(self.menu, (0,100))
						self.screen.blit(self.mute, (0,200))
						self.screen.blit(self.volumeInc, (0,300))
						self.screen.blit(self.volumeDec, (0,400))
						self.screen.blit(self.showTime, (0,500))
						self.screen.blit(self.bug, (0,600))
				if e.type == MOUSEBUTTONDOWN:
					if self.m1.collidepoint(self.pos):
						self.optionsMenu = False
						self.titleScreen()
						print Variables.muted
						self.getGameVersion()
					if self.m2.collidepoint(self.pos):
						if Variables.muted == False:
							Variables.volume = 0.0
							Variables.muted = True
							break
						if Variables.muted == True:
							Variables.volume = 0.2
							Variables.muted = False
							break
					if self.m3.collidepoint(self.pos):
						if Variables.volume <= 0.9:
							Variables.volume += 0.1
							Variables.muted = False
						else:
							Variables.volume = 1.0
					if self.m4.collidepoint(self.pos):
						if Variables.volume >= 0.1:
							Variables.volume -= 0.1
						if Variables.volume < 0.1:
							Variables.volume = 0.0
							Variables.muted = True
					if self.m5.collidepoint(self.pos):
						if Variables.showTime == False:
							Variables.showTime = True
							break
						if Variables.showTime == True:
							Variables.showTime = False
							break
					if self.m6.collidepoint(self.pos):
						result = tkMessageBox.askquestion("Issues Page Launcher", "This will launch a webbrowser directed to the MoT issues page; click 'yes' if you are okay with this or no to cancel.", icon='warning')
						if result == "yes":
							webbrowser.open('http://wepcgame.com/issues/my_view_page.php')
						else:
							break
			pygame.display.update()

	def loadingScreen(self):
		"""Upcoming system to show deaths that level, time taken, etc. """
		self.continueButton = pygame.image.load(Directory().getDirectory() + '/images/intro/play.png')
		self.continueButton2 = pygame.image.load(Directory().getDirectory() + '/images/intro/play2.png')

		# pygame.display.set_caption("Master of Thieves")
		self.background_image = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/backgrounds/background0.png"), (self.WIN_WIDTH, self.WIN_HEIGHT)) # Tutorial background
		self.screen.blit(self.background_image, (0,0))
		self.showTimeTaken()
		pygame.mouse.set_visible(True)
		self.m1 = self.screen.blit(self.continueButton, (0, 75))
		self.loadingStatus = True
		while self.loadingStatus == True:
			for e in pygame.event.get():
				self.pos = pygame.mouse.get_pos()
				if e.type == QUIT:
					exit()
				if e.type == MOUSEMOTION:
					if self.m1.collidepoint(self.pos): # Scrolling over the Main Menu button, so change the image so the user knows they are on it
						self.screen.blit(self.continueButton2, (0, 75))
					else:
						self.screen.blit(self.continueButton, (0, 75)) # Change back to the normal image since the user is no longer on it
				if e.type == MOUSEBUTTONDOWN:
					if self.m1.collidepoint(self.pos):
						self.loadingStatus = False
			pygame.display.update()

	def showTimeTaken(self):
		self.deathsFont = pygame.font.SysFont("Comic Sans MS", 35)
		self.completedLevel = self.deathsFont.render("You took " + str(Variables.total_time) + " seconds to complete the level", True, (0,0,0))
		self.screen.blit(self.completedLevel, (0, 30))

	def preMenu(self):
		pygame.display.set_caption(self.GAMENAME)
		pygame.mouse.set_visible(True)
		self.background_image = pygame.transform.scale(pygame.image.load(Directory().getDirectory() + "/images/intro/premenu.png"), (self.WIN_WIDTH, self.WIN_HEIGHT)) # Tutorial background
		self.screen.blit(self.background_image, (0,0))