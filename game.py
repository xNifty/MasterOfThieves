#! /usr/bin/python

import pygame
import time as pause
from pygame import *
import cgitb
import os
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

from camera import *

pygame.init()

sounds = Sounds()
levelLoader = levelLoader()
Deaths = Deaths()

cgitb.enable(logdir='errors', display=False, format='text')

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
        pygame.display.set_caption("Master of Thieves | Level: " +str(levelLoader.getLevel()) + " | Deaths (level): " + str(Deaths.getLevelDeaths()) + " | Deaths (Total): " + str(Deaths.getDeathsTotal()) + 
            " | FPS: " + str(int(timer.get_fps())))
        asize = ((Display.screen_rect.w // levelLoader.getBGWidth() + 1) * levelLoader.getBGWidth(), (Display.screen_rect.h // levelLoader.getBGHeight() + 1) * levelLoader.getBGHeight())
        bg = pygame.Surface(asize)

        for x in range(0, asize[0], levelLoader.getBGWidth()):
            for y in range(0, asize[1], levelLoader.getBGHeight()):
                Display.screen.blit(levelLoader.getBackground(), (x, y))

        timer.tick(38)

        levelLoader.getPlayer().getKeyPress()

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getCoins(), True, pygame.sprite.collide_mask):
            levelLoader.getPlayer().addCoin()
            print levelLoader.getPlayer().getCoins()
            if sounds.mute == False:
                sounds.coin_sound.play()
                sounds.coin_sound.set_volume(sounds.getVolume())
            levelLoader.getPlayer().canHitCoin = True

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getTrophy(), True, pygame.sprite.collide_mask):
            try:
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
            except:
                print "Exception found; attempting reload of main menu"
                Display.gameOver()
                print "Game Over blit"
                pygame.display.update()
                pause.sleep(5)
                Display.reloadTitleScreen()
                Deaths.resetDeathsTotal()
                levelLoader.resetLevel()
                print Display.title
                print "main menu loaded"
                break

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getSpikes(), False, pygame.sprite.collide_mask) and levelLoader.getPlayer().canDie == True:
            levelLoader.getPlayer().dead = True

        if levelLoader.getPlayer().dead == True:
            levelLoader.reloading = True
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
            if sounds.mute == False:
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
       
Display.titleScreen()
while Display.title == True:
    for e in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if e.type == QUIT: # "X"ed out of the game
            exit()
        if e.type == MOUSEMOTION: # If the user scrolls over one of the buttons change to the image with the red background so that the user knows they are on it
            if Display.b1.collidepoint(pos):
                Display.screen.blit(Display.play2, (0, 100))
            elif Display.b2.collidepoint(pos):
                Display.screen.blit(Display.tut2, (0, 200))
            elif Display.b3.collidepoint(pos):
                Display.screen.blit(Display.exit2, (0, 300))
            else: # Show the orange background image if the user is not scrolled over the image
                Display.screen.blit(Display.play, (0, 100))
                Display.screen.blit(Display.tut, (0, 200))
                Display.screen.blit(Display.exit, (0, 300))
        if e.type == MOUSEBUTTONDOWN:
            if Display.b1.collidepoint(pos):
                Display.title = False
                main() # Clicked to start the game
            if Display.b2.collidepoint(pos):
                Display.tutstatus = True
                Display.tutorial() # Clicked to go to the tutorial screen
            if Display.b3.collidepoint(pos):
                exit()
    pygame.display.update()