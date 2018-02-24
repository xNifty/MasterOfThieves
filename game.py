#! /usr/bin/python

import time as pause
import cgitb
from pygame import *
from sys import exit

from BuildFunctions.sounds import Sounds
from BuildFunctions.themes import Themes
from BuildFunctions.deaths import Deaths
from BuildFunctions.level_loader import LevelLoader
from BuildFunctions.directory import Directory
from BuildFunctions.variables import Variables

from Display.camera import *

pygame.init()

sounds = Sounds()
Deaths = Deaths()
sounds = Sounds()
LevelLoader = LevelLoader()

cgitb.enable(logdir='errors', display=False, format='text')

def main():
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    timer = pygame.time.Clock()

    pygame.mouse.set_visible(False)

    print("Successfully reading from directory: " + Directory().get_directory())
    LevelLoader.buildLevel()
    starting_time = pause.time()
    Variables.canUseKeys = False

    total_level_width = len('level'[0])*32
    total_level_height = len('level')*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    LevelLoader.entities.add(LevelLoader.getPlayer())
    pygame.display.update()
           
    while 1:
        pygame.display.set_caption(Display.gameName() + " | Level: " + str(LevelLoader.get_level()) +
                                   " | Deaths (level): " + str(Deaths.getLevelDeaths()) +
                                   " | Deaths (Total): " + str(Deaths.getDeathsTotal()) +
                                   " | FPS: " + str(int(timer.get_fps()))
                                   )
        asize = (
            (Display.screen_rect.w // LevelLoader.getBGWidth() + 1) * LevelLoader.getBGWidth(),
            (Display.screen_rect.h // LevelLoader.getBGHeight() + 1) * LevelLoader.getBGHeight()
        )

        for x in range(0, asize[0], LevelLoader.getBGWidth()):
            for y in range(0, asize[1], LevelLoader.getBGHeight()):
                Display.screen.blit(LevelLoader.getBackground(), (x, y))

        timer.tick(38)

        if not Variables.loadedTheme:
            Variables.loadedTheme = True
            try:
                print("\nAttempting to choose level specific theme...")
                theme = (Themes(LevelLoader.get_level()))
                print("Level specific theme selection successful.")
            except:
                print("Failed to load level specific theme; attempting default theme...")
                theme = (Themes(0))
                print("Loaded backup theme.")
            pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(Variables.volume)

        coin_collide = pygame.sprite.spritecollide(
            LevelLoader.getPlayer(), LevelLoader.get_coins(), True, pygame.sprite.collide_mask
        )
        for coin in coin_collide:
            if coin:
                LevelLoader.getPlayer().add_coin()
                sounds.coin_sound.play()
                sounds.coin_sound.set_volume(Variables.volume)

        if pygame.sprite.spritecollide(LevelLoader.getPlayer(), LevelLoader.getTrophy(), True, pygame.sprite.collide_mask):
            if Variables.showTime:
                print("getting time for level: " + str(LevelLoader.get_level()))
                end_time = pause.time()
                Variables.total_time = float("{0:.2f}".format(end_time - starting_time))
                print(str(Variables.total_time))
                Display.loadingScreen()
                pygame.mouse.set_visible(False)
            try:
                # @TODO : this block needs to change from try..catch for switching the level to a clean method
                # @TODO : we need to be able to catch errors for actual logging to find out why something broke
                Variables.loadedTheme = False
                Variables.canUseKeys = False
                LevelLoader.add_level()
                Display.loadingLevel(LevelLoader.get_level())
                Deaths.resetLevelDeaths()
                LevelLoader.rebuildDoors()
                LevelLoader.getPlayer().reset_coins()
                LevelLoader.clear_screen()
                pygame.display.update()
                LevelLoader.rebuild_objects()
                pause.sleep(5)
                LevelLoader.buildLevel()
                LevelLoader.entities.add(LevelLoader.getPlayer())
                starting_time = pause.time()
            except Exception as ex:
                print(ex)
                Display.gameOver()
                pygame.display.update()
                pause.sleep(5)
                Display.reloadTitleScreen()
                Deaths.resetDeathsTotal()
                LevelLoader.reset_level()
                pygame.mixer.music.stop()
                break

        if pygame.sprite.spritecollide(LevelLoader.getPlayer(), LevelLoader.getSpikes(), False, pygame.sprite.collide_mask) and LevelLoader.getPlayer().canDie == True:
            LevelLoader.getPlayer().dead = True

        if LevelLoader.getPlayer().dead:
            Variables.canUseKeys = False
            LevelLoader.rebuildDoors()
            Deaths.addDeaths()
            LevelLoader.getPlayer().reset_coins()
            LevelLoader.clear_screen()
            pygame.display.update()
            LevelLoader.rebuild_objects()
            pause.sleep(1)
            LevelLoader.buildLevel()
            LevelLoader.entities.add(LevelLoader.getPlayer())

        if LevelLoader.getPlayer().get_coins() >= LevelLoader.get_level_coins() and LevelLoader.doorStatus() == True:
            sounds.door.play()
            sounds.door.set_volume(Variables.volume)
            for x in range(2):
                LevelLoader.delPlatforms()
            LevelLoader.delDoors()

        camera.update(LevelLoader.getPlayer())

        LevelLoader.getPlayer().update(
            LevelLoader.getPlayer().up,
            LevelLoader.getPlayer().left,
            LevelLoader.getPlayer().right,
            LevelLoader.getPlatforms()
        )
        for ent in LevelLoader.getEntities():
            Display.screen.blit(ent.image, camera.apply(ent))

        if Variables.canUseKeys:
            LevelLoader.getPlayer().get_key_press()

        Display.getGameVersion()
        LevelLoader.infoScreen()
        pygame.display.update()
        Variables.canUseKeys = True


#Display.preMenu()
#pygame.display.update()
#pause.sleep(5)
Display.titleScreen()
Display.getGameVersion()
while Display.title:
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
