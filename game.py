#! /usr/bin/python

import pygame
import time as pause
from pygame import *
import cgitb
from sys import exit
import pygame._view

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
from directory import Directory
from camera import *
from variables import Variables

pygame.init()

sounds = Sounds()
levelLoader = levelLoader()
Deaths = Deaths()
sounds = Sounds()

cgitb.enable(logdir='errors', display=False, format='text')

def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    timer = pygame.time.Clock()

    pygame.mouse.set_visible(False)

    print "Successfully reading from directory: " + Directory().getDirectory()
    levelLoader.buildLevel()
    starting_time = pause.time()
    Variables.canUseKeys = False

    total_level_width  = len('level'[0])*32
    total_level_height = len('level')*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    levelLoader.entities.add(levelLoader.getPlayer())
    pygame.display.update()
           
    while 1:
        pygame.display.set_caption("Master of Thieves | Level: " +str(levelLoader.getLevel()) + " | Deaths (level): " + str(Deaths.getLevelDeaths()) + 
            " | Deaths (Total): " + str(Deaths.getDeathsTotal()) + " | FPS: " + str(int(timer.get_fps())))
        asize = ((Display.screen_rect.w // levelLoader.getBGWidth() + 1) * levelLoader.getBGWidth(), (Display.screen_rect.h // levelLoader.getBGHeight() + 1) * levelLoader.getBGHeight())

        for x in range(0, asize[0], levelLoader.getBGWidth()):
            for y in range(0, asize[1], levelLoader.getBGHeight()):
                Display.screen.blit(levelLoader.getBackground(), (x, y))

        timer.tick(38)

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getCoins(), True, pygame.sprite.collide_mask):
            levelLoader.getPlayer().addCoin()
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(Variables.volume)

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getTrophy(), True, pygame.sprite.collide_mask):
            if Variables.showTime == True:
                print "getting time!"
                end_time = pause.time()
                Variables.total_time = float("{0:.2f}".format(end_time - starting_time))
                print str(Variables.total_time)
                Display.loadingScreen()
                pygame.mouse.set_visible(False)
            try:
                Variables.loadedTheme = False
                Variables.canUseKeys = False
                levelLoader.addLevel()
                Display.loadingLevel(levelLoader.getLevel())
                Deaths.resetLevelDeaths()
                levelLoader.rebuildDoors()
                levelLoader.getPlayer().resetCoins()
                levelLoader.clearScreen()
                pygame.display.update()
                levelLoader.rebuildObjects()
                pause.sleep(5)
                levelLoader.buildLevel()
                levelLoader.entities.add(levelLoader.getPlayer())
                starting_time = pause.time()
            except:
                Display.gameOver()
                pygame.display.update()
                pause.sleep(5)
                Display.reloadTitleScreen()
                Deaths.resetDeathsTotal()
                levelLoader.resetLevel()
                pygame.mixer.music.stop()
                break

        if Variables.muted == False and Variables.loadedTheme == False:
            Variables.loadedTheme = True
            try:
                print "\nAttempting to choose level specific theme..."
                theme = (Themes(levelLoader.getLevel()))
            except:
                print "Failed to load level specific theme; attempting default theme..."
                theme = (Themes(0))
            pygame.mixer.music.set_volume(Variables.volume)
            pygame.mixer.music.play(-1, 0.0)
            print "Theme selection successful."

        if Variables.muted == True:
            Variables.volume = 0.0
            pygame.mixer.music.stop()
            Variables.loadedTheme = False

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getSpikes(), False, pygame.sprite.collide_mask) and levelLoader.getPlayer().canDie == True:
            levelLoader.getPlayer().dead = True

        if levelLoader.getPlayer().dead == True:
            Variables.canUseKeys = False
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
            sounds.door.set_volume(Variables.volume)
            for x in xrange(2):
                levelLoader.delPlatforms()
            levelLoader.delDoors()

        camera.update(levelLoader.getPlayer())

        levelLoader.getPlayer().update(levelLoader.getPlayer().up, levelLoader.getPlayer().left, levelLoader.getPlayer().right, levelLoader.getPlatforms())
        for e in levelLoader.getEntities():
            Display.screen.blit(e.image, camera.apply(e))

        if Variables.canUseKeys == True:
            levelLoader.getPlayer().getKeyPress()

        Display.getGameVersion()
        levelLoader.infoScreen()
        pygame.display.update()
        Variables.canUseKeys = True

Display.titleScreen()
Display.getGameVersion()
while Display.title == True:
    for e in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if e.type == QUIT:
            exit()
        if e.type == MOUSEMOTION:
            if Display.b1.collidepoint(pos):
                Display.screen.blit(Display.play2, (0,100))
            elif Display.b2.collidepoint(pos):
                Display.screen.blit(Display.tut2, (0,200))
            elif Display.b3.collidepoint(pos):
                Display.screen.blit(Display.options2, (0,300))
            elif Display.b4.collidepoint(pos):
                Display.screen.blit(Display.exit2, (0,400))
            else:
                Display.screen.blit(Display.play, (0,100))
                Display.screen.blit(Display.tut, (0,200))
                Display.screen.blit(Display.options, (0,300))
                Display.screen.blit(Display.exit, (0,400))
        if e.type == MOUSEBUTTONDOWN:
            if Display.b1.collidepoint(pos):
                Display.title = False
                main()
            if Display.b2.collidepoint(pos):
                Display.tutstatus = True
                Display.tutorial()
            if Display.b3.collidepoint(pos):
                Display.optionsMenu = True
                Display.optionsScreen()
            if Display.b4.collidepoint(pos):
                exit()
    pygame.display.update()