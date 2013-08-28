# Handles death counting; temporary?

class Deaths(object):
	def __init__(self):
		self.deaths = 0
		self.levelDeaths = 0

	def getLevelDeaths(self):
		return self.levelDeaths

	def getDeathsTotal(self):
		return self.deaths

	def addDeaths(self):
		self.deaths += 1
		self.levelDeaths += 1

	def resetLevelDeaths(self):
		self.levelDeaths = 0

	def resetDeathsTotal(self):
		self.deaths = 0