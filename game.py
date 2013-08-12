#! /usr/bin/python

import pygame
import os
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

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

sounds = Sounds()
levelLoader = levelLoader()
Deaths = Deaths()

def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    screen = pygame.display.set_mode(Display.getDisplay(), Display.getFlags(), Display.getDepth())
    screen_rect = screen.get_rect()
    timer = pygame.time.Clock()

    show_debug = False

    pygame.mouse.set_visible(False)

    sounds = Sounds()

    font = pygame.font.SysFont("arial", 25)

    up = left = right = running = False

    levelLoader.buildLevel()
    try:
        theme = (Themes(levelLoader.getLevel()))
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(sounds.getVolume())
    except:
        theme = (Themes(0))
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(sounds.getVolume())

    total_level_width  = len('level'[0])*32
    total_level_height = len('level')*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    levelLoader.entities.add(levelLoader.getPlayer())
           
    while 1:
        pygame.display.set_caption("Master of Thieves | Level: " +str(levelLoader.getLevel()) + " | Deaths (level): " + str(Deaths.getLevelDeaths()) + " | Deaths (Total): " + str(Deaths.getDeathsTotal()) + " | FPS: " + str(int(timer.get_fps())))
        asize = ((screen_rect.w // levelLoader.getBGWidth() + 1) * levelLoader.getBGWidth(), (screen_rect.h // levelLoader.getBGHeight() + 1) * levelLoader.getBGHeight())
        bg = pygame.Surface(asize)

        for x in range(0, asize[0], levelLoader.getBGWidth()):
            for y in range(0, asize[1], levelLoader.getBGHeight()):
                screen.blit(levelLoader.getBackground(), (x, y))

        timer.tick(38)

        for e in pygame.event.get():
            if e.type == QUIT: 
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            if e.type == KEYDOWN and e.key == K_SPACE:
                levelLoader.getPlayer().onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_UP:
                levelLoader.getPlayer().onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                levelLoader.getPlayer().direction = 'left'
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                levelLoader.getPlayer().direction = 'right'
                right = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            if e.type == KEYDOWN and e.key == K_w:
                levelLoader.getPlayer().onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                levelLoader.getPlayer().direction = 'left'
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                levelLoader.getPlayer().direction = 'right'
                right = True
            if e.type == KEYDOWN and e.key == K_RETURN:
                levelLoader.getPlayer().dead = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                if levelLoader.getPlayer().canDie == True:
                    levelLoader.getPlayer().canDie = False
                    break
                if levelLoader.getPlayer().canDie == False:
                    levelLoader.getPlayer().canDie = True
                    break
            if e.type == KEYDOWN and e.key == K_i:
                if show_debug == False:
                    show_debug = True
                    break
                if show_debug == True:
                    show_debug = False
                    break
            if e.type == KEYDOWN and e.key == K_c:
                levelLoader.getPlayer().setCoins()
            if e.type == KEYDOWN and e.key == K_e:
                levelLoader.getPlayer().yvel -= 20

            if e.type == KEYUP and e.key == K_SPACE:
                levelLoader.getPlayer().onGround = True
                up = False
            if e.type == KEYUP and e.key == K_UP:
                levelLoader.getPlayer().onGround = True
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                levelLoader.getPlayer().direction = 'right'
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                levelLoader.getPlayer().direction = 'left'
                left = False
            if e.type == KEYUP and e.key == K_w:
                levelLoader.getPlayer().onGround = True
                up = False
            if e.type == KEYUP and e.key == K_d:
                levelLoader.getPlayer().direction = 'right'
                right = False
            if e.type == KEYUP and e.key == K_a:
                levelLoader.getPlayer().direction = 'left'
                left = False

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getCoins(), True, pygame.sprite.collide_mask):
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(sounds.getVolume())
            levelLoader.getPlayer().addCoin()

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getTrophy(), True, pygame.sprite.collide_mask):
            levelLoader.addLevel()
            print levelLoader.getLevel()
            loading = font.render("Loading level: " + str(levelLoader.getLevel()), True, (255,255,255))
            screen.blit(levelLoader.loadingBar, (0,0))
            screen.blit(loading, (0,0))
            Deaths.resetLevelDeaths()
            levelLoader.getPlayer().onGround = True
            levelLoader.rebuildDoors()
            up = False
            right = False
            left = False
            levelLoader.getPlayer().resetCoins()
            levelLoader.clearScreen()
            pygame.display.update()
            levelLoader.rebuildObjects()
            pause.sleep(5)
            levelLoader.buildLevel()
            levelLoader.entities.add(levelLoader.getPlayer())
            try:
                theme = (Themes(levelLoader.getLevel()))
                pygame.mixer.music.play(-1, 0.0)
                pygame.mixer.music.set_volume(sounds.getVolume())
            except:
                theme = (Themes(0))
                pygame.mixer.music.play(-1, 0.0)
                pygame.mixer.music.set_volume(sounds.getVolume())

        if pygame.sprite.spritecollide(levelLoader.getPlayer(), levelLoader.getSpikes(), False, pygame.sprite.collide_mask) and levelLoader.getPlayer().canDie == True:
            levelLoader.getPlayer().dead = True

        if levelLoader.getPlayer().dead == True:
            levelLoader.getPlayer().onGround = True
            levelLoader.rebuildDoors()
            up = False
            right = False
            left = False
            Deaths.addDeaths()
            levelLoader.getPlayer().resetCoins()
            levelLoader.clearScreen()
            pygame.display.update()
            levelLoader.rebuildObjects()
            pause.sleep(1)
            levelLoader.buildLevel()
            levelLoader.entities.add(levelLoader.getPlayer())

        if levelLoader.getPlayer().getCoins() >= 4 and levelLoader.doorStatus() == True:
            sounds.door.play()
            sounds.door.set_volume(sounds.getVolume())
            for x in xrange(2):
                levelLoader.delPlatforms()
            levelLoader.delDoors()
            pygame.display.update()

        camera.update(levelLoader.getPlayer())

        levelLoader.getPlayer().update(up, left, right, levelLoader.getPlatforms())
        for e in levelLoader.getEntities():
            screen.blit(e.image, camera.apply(e))

        if show_debug == True:
            font = pygame.font.SysFont("arial", 25)
            debug = font.render("Information Window", True, (255,255,255))
            death_status = font.render("player.canDie: " + str(levelLoader.getPlayer().canDie), True, (255,255,255))
            door_status = font.render("door_closed: " + str(levelLoader.doorStatus()), True, (255,255,255))
            coin_debug = font.render("coin_count: " + str(levelLoader.getPlayer().getCoins()), True, (255,255,255))
            screen.blit(debug, (0,0))
            screen.blit(death_status, (0,25))
            screen.blit(door_status, (0,50))
            screen.blit(coin_debug, (0,75))

        pygame.display.update()
   
main()