import pygame
from BuildFunctions.directory import Directory

pygame.init()

class Sounds(object):

    def __init__(self):
        """Handles loading the sound files; they are called by doing sounds.NAME in the game class."""
        self.coin_sound = pygame.mixer.Sound(Directory().get_directory() + '/sounds/game/coin_sound.wav')
        #self.death_sound = pygame.mixer.Sound(Directory().get_directory() + '/sounds/game/death.wav')
        self.door = pygame.mixer.Sound(Directory().get_directory() + '/sounds/game/door.wav')