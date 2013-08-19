class Directory(object):
	def __init__(self):
		# self.dir = 'data2'
		with open('directory.txt', 'r') as f:
			self.dir = f.readline()

	def getDirectory(self):
		return self.dir