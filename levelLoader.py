# Read about what each thing does in the respective class
# !!! WARNING !!! The game will break if the level does not contain the player ("C") within; the game may break if the door Top and Bottom is not found as well.

import pygame
from pygame.locals import *
import re

from entities import Entity
from player import Player
from platform import Platform
from door import Door
from coins import Coins
from spike import Spike
from sounds import Sounds
from trophies import Trophy
from themes import Themes
from display import Display

Display = Display()

class levelLoader(object):
	""" 
	This class actually handles a lot of things; while also handling the level loading, it also must be used to call from another class in the game
	class itself.  For example, to use anything from the Player class, the user must have levelLoader.getPlayer().functionHere.
	In all honesty, this class handles pretty much everything that has anything to do with levels.
	"""
	def __init__(self):
		self.level = 20
		self.platforms = []

		self.doorsClosed = True

		self.entities = pygame.sprite.Group()
		self.coin = pygame.sprite.Group()
		self.spikes = pygame.sprite.Group()
		self.trophies = pygame.sprite.Group()
		self.x = 0
		self.y = 0

		self.show_debug = False

		self.loadingBar = pygame.transform.scale(pygame.image.load("images/button.png"), (Display.getWinWidth(), 35))

		self.levelCoins = 0

	def buildLevel(self):
		"""
		KEY FOR LEVELS
        P = Platform
        C = player starting position
        A = Spike (Up) - 1
        V = Spike (Down) - 2
        > = Spike (Right) - 3
        < = Spike (Left) - 4
        K = Key
        X = Trophy
        T = Door Top
        B = Door Bottom
        O = Coin
        """
		try:
			level = open('levels/level' + str(self.level) + '.txt', 'r')
		except:
			self.level = 0
			level = open('levels/level0.txt', 'r')
		for row in level:
		    for col in row:
		    	if col.isdigit():
		    		if int(col) > 0:
		    			print "found number: " + str(col)
		    			self.levelCoins = int(col)
		    			print self.levelCoins
		    		else:
		    			print "got no coin amount...assuming a set of 1"
		    			self.levelCoins = 1
		    			print self.levelCoins
		        if col == "P":
		            p = Platform(self.x, self.y) # Place a platform at the given x,y
		            self.platforms.insert(0, p) # Insert it into the platforms list
		            self.entities.add(p) # Add to entities so it appears on screen
		        if col == "C":
					#print "Character found!"
					self.charX = self.x # The character x found from file loading
					self.charY = self.y # The character y found from file loading
					self.player = Player(self.charX, self.charY) # Set the player along with the x,y of the starting position
					#print "yes, player!"
		        if col == "A":
		            spike = Spike(self.x, self.y, 1) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == "V":
		            spike = Spike(self.x, self.y, 2) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == ">":
		            spike = Spike(self.x, self.y, 3) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == "<":
		            spike = Spike(self.x, self.y, 4) # Load a spike at the x,y found 
		            self.entities.add(spike) # Add the spike to the entities
		            self.spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
		        if col == "O":
		            coin = Coins(self.x, self.y) # Load a coin image at the given x,y
		            self.entities.add(coin) # Coin 1 to the entities
		            self.coin.add(coin) # add coin 1 to the coinA sprite group
		        if col == "X":
		            win_object = Trophy(self.x, self.y, self.level) # Load the proper trophy by passing the level to the trophy class and load at the given x,y from file loading
		            self.entities.add(win_object) # Add the trophy to the entities so it appears
		            self.trophies.add(win_object) # Also make it a trophy sprite for collision detection purposes
		        if col == "T":
		            self.doorA = Door(self.x, self.y)
		            self.platforms.append(self.doorA) # Make the door top a platform so the player cannot walk through it
		            self.entities.add(self.doorA) # Add the door bottom to the entities
		        if col == "B":
		            self.doorB = Door(self.x, self.y)
		            self.platforms.append(self.doorB) # Make the door bottom a platform so the player cannot walk through it
		            self.entities.add(self.doorB) # Add the door bottom to entities
		        self.x += 32
		    self.y += 32
		    self.x = 0

		# Try loading in the level image and theme; if it fails, use level 0 theme and background
		try:
		    self.background = pygame.image.load('images/backgrounds/background' + str(self.level) + '.png').convert_alpha()
		    self.background_rect = self.background.get_rect()
		except:
		    self.background = pygame.image.load('images/backgrounds/background0.png').convert_alpha()
		    self.background_rect = self.background.get_rect()

	def getPlayer(self):
		return self.player

	def getPlatforms(self):
		return self.platforms

	def getEntities(self):
		return self.entities

	def getCoins(self):
		return self.coin

	def getTrophy(self):
		return self.trophies

	def getSpikes(self):
		return self.spikes

	def getBGWidth(self):
		return self.background_rect.w

	def getBGHeight(self):
		return self.background_rect.h

	def getBackground(self):
		return self.background

	def delPlatforms(self):
		del self.platforms[-1]

	def delDoors(self):
		self.doorsClosed = False
		self.doorA.kill()
		self.doorB.kill()

	def rebuildDoors(self):
		self.doorsClosed = True

	def doorStatus(self):
		return self.doorsClosed

	def clearScreen(self):
		self.player.onGround = True
		self.x = 0
		self.y = 0
		level = self.level
		self.platforms = None
		self.doorA.kill()
		self.doorB.kill()
		self.entities.empty()
		self.trophies.empty()
		self.spikes.empty()
		self.coin.empty()

	def rebuildObjects(self):
		self.level = self.level
		self.platforms = []
		self.doorsClosed = True
		self.player = Player(self.charX, self.charY)
		self.entities = pygame.sprite.Group()
		self.coin = pygame.sprite.Group()
		self.spikes = pygame.sprite.Group()
		self.trophies = pygame.sprite.Group()
		self.x = 0
		self.y = 0
		self.player.dead = False
		self.player.up = False
		self.player.right = False
		self.player.left = False
		self.player.running = False

	def addLevel(self):
		self.level += 1

	def getLevel(self):
		return self.level

	def loadingBar(self):
		return self.loadingBar

	def getLevelCoins(self):
		return self.levelCoins