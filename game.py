#! /usr/bin/python

import pygame
import time as pause
from pygame import *
from sys import exit

from entities import Entity
from player import Player
from platform import Platform
from door import Door
from coins import Coins
from spike import Spike
from sounds import Sounds
from trophies import Trophy
from themes import Themes
from deaths import Deaths
from levelLoader import levelLoader

from camera import *

pygame.init()

sounds = Sounds()
levelLoader = levelLoader()
Deaths = Deaths()

def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    timer = pygame.time.Clock()

    pygame.mouse.set_visible(False)

    sounds = Sounds()

    levelLoader.buildLevel()
    try:
        if sounds.mute == False:
            theme = (Themes(levelLoader.getLevel()))
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(sounds.getVolume())
    except:
        if sounds.mute == False:
            theme = (Themes(0))
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(sounds.getVolume())

    total_level_width  = len('level'[0])*32
    total_level_height = len('level')*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    levelLoader.entities.add(levelLoader.getPlayer())
           
    while 1:
        pygame.display.set_caption("Master of Thieves | Level: " +str(levelLoader.getLevel()) + " | Deaths (level): " + str(Deaths.getLevelDeaths()) + " | Deaths (Total): " + str(Deaths.getDeathsTotal()) + " | FPS: " + str(int(timer.get_fps())))
        asize = ((Display.screen_rect.w // levelLoader.getBGWidth() + 1) * levelLoader.getBGWidth(), (Display.screen_rect.h // levelLoader.getBGHeight() + 1) * levelLoader.getBGHeight())
        bg = pygame.Surface(asize)

        for x in range(0, asize[0], levelLoader.getBGWidth()):
            for y in range(0, asize[1], levelLoader.getBGHeight()):
                Display.screen.blit(levelLoader.getBackground(), (x, y))

        timer.tick(38)

        levelLoader.getPlayer().getKeyPress()

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getCoins(), True, pygame.sprite.collide_mask):
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(sounds.getVolume())
            levelLoader.getPlayer().addCoin()

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getTrophy(), True, pygame.sprite.collide_mask):
            levelLoader.addLevel()
            loading = Display.font.render("Loading level: " + str(levelLoader.getLevel()), True, (255,255,255))
            Display.screen.blit(Display.loadingBar, (0,0))
            Display.screen.blit(loading, (10,0))
            Deaths.resetLevelDeaths()
            levelLoader.getPlayer().onGround = True
            levelLoader.rebuildDoors()
            levelLoader.getPlayer().resetCoins()
            levelLoader.clearScreen()
            pygame.display.update()
            levelLoader.rebuildObjects()
            pause.sleep(5)
            levelLoader.buildLevel()
            print "Loaded level: " + str(levelLoader.getLevel())
            levelLoader.entities.add(levelLoader.getPlayer())
            try:
                if sounds.mute == False:
                    theme = (Themes(levelLoader.getLevel()))
                    pygame.mixer.music.play(-1, 0.0)
                    pygame.mixer.music.set_volume(sounds.getVolume())
            except:
                if sounds.mute == False:
                    theme = (Themes(0))
                    pygame.mixer.music.play(-1, 0.0)
                    pygame.mixer.music.set_volume(sounds.getVolume())

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getSpikes(), False, pygame.sprite.collide_mask) and levelLoader.getPlayer().canDie == True:
            levelLoader.getPlayer().dead = True

        if levelLoader.getPlayer().dead == True:
            levelLoader.getPlayer().onGround = True
            levelLoader.rebuildDoors()
            Deaths.addDeaths()
            levelLoader.getPlayer().resetCoins()
            levelLoader.clearScreen()
            pygame.display.update()
            levelLoader.rebuildObjects()
            pause.sleep(1)
            levelLoader.buildLevel()
            levelLoader.entities.add(levelLoader.getPlayer())

        if levelLoader.getPlayer().getCoins() >= levelLoader.getLevelCoins() and levelLoader.doorStatus() == True:
            sounds.door.play()
            sounds.door.set_volume(sounds.getVolume())
            for x in xrange(2):
                levelLoader.delPlatforms()
            levelLoader.delDoors()

        camera.update(levelLoader.getPlayer())

        levelLoader.getPlayer().update(levelLoader.getPlayer().up, levelLoader.getPlayer().left, levelLoader.getPlayer().right, levelLoader.getPlatforms())
        for e in levelLoader.getEntities():
            Display.screen.blit(e.image, camera.apply(e))

        pygame.display.update()
   
main()