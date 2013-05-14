#! /usr/bin/python

import pygame
import gc # garbage collector
import os
import time as pause
from pygame import *
from sys import exit

# Import all of our classes
from entities import Entity
from player import Player
from platform import Platform
from door import Door
from coins import Coins
from spike import Spike
from sounds import Sounds
from trophies import Trophy
from themes import Themes

from camera import *

os.environ['SDL_VIDEO_CENTERED'] = '1' # Attempt to center the game window on the users screen; may not always work

# The below globals are used throughout; disliked them, but they wouldn't work any other way.
global coin_count, delete_door, current_level, deaths, deaths_total, volume
current_level = 0
deaths = 0
deaths_total = 0
coin_count = 0
delete_door = True
volume = 0.2 # Maximum volume

# Initialize PyGame
pygame.init()

# The menu music; ends when the first level begins
pygame.mixer.pre_init(44100, -16, 2, 2048)
sounds = Sounds()
theme = (Themes(-1)) # Themes(-1) is the theme name within the /sounds/themes folder
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(volume)

def titleScreen():
    """This function handles the title screen display; from it, the user can start the game, view the tutorial, or exit."""
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH) # information comes from the camera class
    screen_rect = screen.get_rect() # get the screen rect
    pygame.display.set_caption("Master of Thieves") # Window caption
    background_image = pygame.transform.scale(pygame.image.load("images/intro/title_bg.png"), (WIN_WIDTH, WIN_HEIGHT)) # Load the title background

    # All of the button images
    play = pygame.image.load('images/intro/play.png')
    play2 = pygame.image.load('images/intro/play2.png')
    exit = pygame.image.load('images/intro/exit.png')
    exit2 = pygame.image.load('images/intro/exit2.png')
    tut = pygame.image.load('images/intro/tutorial.png')
    tut2 = pygame.image.load('images/intro/tutorial2.png')

    # Blit the initial images to the screen; order: PLAY, TUT, EXIT
    screen.blit(background_image, (0,0))
    b1 = screen.blit(play, (0, 100))
    b2 = screen.blit(tut, (0, 200))
    b3 = screen.blit(exit, (0, 300))
    title = True # Title status is true while the game waits for the user to make a choice

    # We want the cursor on the main menu and tutorial screen.
    pygame.mouse.set_visible(True)

    # Keep the title screen looping while the user makes a decision; checks for clicking within a image to perform the action (color changes when scrolled over)
    while title == True:
        for e in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if e.type == QUIT: # "X"ed out of the game
                raise SystemExit()
            if e.type == MOUSEMOTION: # If the user scrolls over one of the buttons change to the image with the red background so that the user knows they are on it
                if b1.collidepoint(pos):
                    screen.blit(play2, (0, 100))
                elif b2.collidepoint(pos):
                    screen.blit(tut2, (0, 200))
                elif b3.collidepoint(pos):
                    screen.blit(exit2, (0, 300))
                else: # Show the orange background image if the user is not scrolled over the image
                    screen.blit(play, (0, 100))
                    screen.blit(tut, (0, 200))
                    screen.blit(exit, (0, 300))
            if e.type == MOUSEBUTTONDOWN:
                if b1.collidepoint(pos):
                    title = False
                    main() # Clicked to start the game
                if b2.collidepoint(pos):
                    tutorial() # Clicked to go to the tutorial screen
                if b3.collidepoint(pos):
                    raise SystemExit() # Exit

        pygame.display.update() # Update the display

def tutorial():
    """This function handles the tutorial window."""
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    screen_rect = screen.get_rect()
    pygame.display.set_caption("Master of Thieves")
    background_image = pygame.transform.scale(pygame.image.load("images/intro/tutscreen.png"), (WIN_WIDTH, WIN_HEIGHT)) # Tutorial background
    screen.blit(background_image, (0,0))

    # Menu buttons
    menu = pygame.image.load('images/intro/menu.png')
    menu2 = pygame.image.load('images/intro/menu2.png')

    m1 = screen.blit(menu, (0,0))
    tutstatus = True

    # Continue running while the status is True
    while tutstatus == True:
        for e in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if e.type == QUIT: # "X"ed out of the game
                raise SystemExit()
            if e.type == MOUSEMOTION:
                if m1.collidepoint(pos): # Scrolling over the Main Menu button, so change the image so the user knows they are on it
                    screen.blit(menu2, (0,0))
                else:
                    screen.blit(menu, (0,0)) # Change back to the normal image since the user is no longer on it
            if e.type == MOUSEBUTTONDOWN:
                if m1.collidepoint(pos):
                    titleScreen() # Clicked to go back to main menu
        pygame.display.update()


def main():
    """The main loop of the game.  It handles loading the levels, key strokes, playing music and sounds; relies heavily on multiple other classes to function correctly.
        These include the camera, coins, door, entities, platform, player, sounds, spike, themes, and trophies classes."""
    gc.enable() # Garbage collector
    global cameraX, cameraY, coin_count, delete_door, current_level, deaths, deaths_total, volume # Load in the global variables
    pygame.mixer.pre_init(44100, -16, 2, 2048) # Initilize the music
    screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH) # Set the screen information
    screen_rect = screen.get_rect()
    timer = pygame.time.Clock()

    # We don't want to see the normal mouse cursor while playing.
    pygame.mouse.set_visible(False)

    sounds = Sounds() # Allows us to call sounds by doing sounds.name

    font = pygame.font.SysFont("arial", 25) # Font for the game

    loading_bar = pygame.transform.scale(pygame.image.load("images/button.png"), (WIN_WIDTH, 35)) # Loading bar image (so that the "Loading Level (level)..." text is visible)

    up = down = left = right = running = False # Set all key strokes (directions) to False


    # Load in the first level by assigning sprites into groups and into the platforms and coin_list lists
    # Read about what each thing does in the respective class
    # !!! WARNING !!! The game will break if the level does not contain the player ("C") within; the game may break if the door Top and Bottom is not found as well.
    """KEY FOR LEVELS
        P = Platform
        C = player starting position
        A = Spike
        1 = coin1
        2 = coin2
        3 = coin3
        4 = coin4
        X = Trophy
        T = Door Top
        B = Door Bottom"""

    platforms = []
    coin_list = []

    entities = pygame.sprite.Group()
    coinA = pygame.sprite.Group()
    coinB = pygame.sprite.Group()
    coinC = pygame.sprite.Group()
    coinD = pygame.sprite.Group()
    spikes = pygame.sprite.Group()
    trophies = pygame.sprite.Group()
    x = 0
    y = 0
    level = open('levels/level' + str(current_level) + '.txt', 'r')
    for row in level:
        for col in row:
            if col == "P":
                p = Platform(x, y) # Place a platform at the given x,y
                platforms.insert(0, p) # Insert it into the platforms list
                entities.add(p) # Add to entities so it appears on screen
            if col == "C":
                charX = x # The character x found from file loading
                charY = y # The character y found from file loading
                player = Player(charX, charY) # Set the player along with the x,y of the starting position
            if col == "A":
                spike = Spike(x, y) # Load a spike at the x,y found 
                entities.add(spike) # Add the spike to the entities
                spikes.add(spike) # Add the spike to the spike sprite group for collison purposes
            if col == "1":
                c1 = Coins(x, y) # Load a coin image at the given x,y
                entities.add(c1) # Coin 1 to the entities
                coin_list.append(c1) # Coin list addition
                coinA.add(c1) # add coin 1 to the coinA sprite group
            if col == "2":
                c2 = Coins(x, y) # Load a coin image at the given x,y
                entities.add(c2) # Coin 2 to the entities
                coin_list.append(c2) # Coin list addition
                coinB.add(c2) # add coin 2 to the coinB sprite group
            if col == "3":
                c3 = Coins(x, y) # Load a coin image at the given x,y
                entities.add(c3) # Coin 3 to the entities
                coin_list.append(c3) # Coin list addition
                coinC.add(c3) # add coin 3 to the coinC sprite group
            if col == "4":
                c4 = Coins(x, y) # Load a coin image at the given x,y
                entities.add(c4) # Coin 4 to the entities
                coin_list.append(c4) # Coin list addition
                coinD.add(c4) # add coin 4 to the coinD sprite group
            if col == "X":
                win_object = Trophy(x, y, current_level) # Load the proper trophy by passing the current_level to the trophy class and load at the given x,y from file loading
                entities.add(win_object) # Add the trophy to the entities so it appears
                trophies.add(win_object) # Also make it a trophy sprite for collision detection purposes
            if col == "T":
                doorA = Door(x, y)
                platforms.append(doorA) # Make the door top a platform so the player cannot walk through it
                entities.add(doorA) # Add the door bottom to the entities
            if col == "B":
                doorB = Door(x, y)
                platforms.append(doorB) # Make the door bottom a platform so the player cannot walk through it
                entities.add(doorB) # Add the door bottom to entities
            x += 32
        y += 32
        x = 0

    # Try loading in the level image and theme; if it fails, use level 0 theme and background
    try:
        theme = (Themes(current_level))
        background = pygame.image.load('images/backgrounds/background' + str(current_level) + '.png').convert_alpha()
        background_rect = background.get_rect()
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(volume)
    except:
        theme = (Themes(0)) # Instead of passing current_level we explicity pass level 0 as we know it exists (unless the user deletes it)
        background = pygame.image.load('images/backgrounds/background0.png').convert_alpha()
        background_rect = background.get_rect()
        pygame.mixer.music.play(-1, 0.0) # Endlessly loop the music
        pygame.mixer.music.set_volume(volume) # Set the music volume

    total_level_width  = len('level'[0])*32
    total_level_height = len('level')*32
    camera = Camera(complex_camera, total_level_width, total_level_height)
    entities.add(player) # Finally, add player to entities so it appears
        
    # The main loop of the game which runs it until we're done.    
    while 1:
        pygame.display.set_caption("Master of Thieves | Deaths (level): " + str(deaths) + " | Deaths (Total): " + str(deaths_total) + " | FPS: " + str(int(timer.get_fps())))
        asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)
        bg = pygame.Surface(asize)

        # Create the background
        for x in range(0, asize[0], background_rect.w):
            for y in range(0, asize[1], background_rect.h):
                screen.blit(background, (x, y))

        timer.tick(38) # The maximum framerate; the game is designed to run at an FPS of 30-40 (38 being best)

        # All the keystroke events; the game can run using the UP-RIGHT-LEFT arrow keys, Space Bar, and the AWD keys (down is never needed)
        #   ENTER will kill the player (used if the player glitch spawns outside the level or glitch out (reloads the level as if they died))
        for e in pygame.event.get():
            if e.type == QUIT: 
                exit()
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            if e.type == KEYDOWN and e.key == K_SPACE:
                player.onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_UP:
                player.onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                player.direction = 'left'
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                player.direction = 'right'
                right = True
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                exit()
            if e.type == KEYDOWN and e.key == K_w:
                player.onGround = False
                up = True
            if e.type == KEYDOWN and e.key == K_a:
                player.direction = 'left'
                left = True
            if e.type == KEYDOWN and e.key == K_d:
                player.direction = 'right'
                right = True
            if e.type == KEYDOWN and e.key == K_RETURN:
                player.dead = True

            if e.type == KEYUP and e.key == K_SPACE:
                player.onGround = True
                up = False
            if e.type == KEYUP and e.key == K_UP:
                player.onGround = True
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                player.direction = 'right'
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                player.direction = 'left'
                left = False
            if e.type == KEYUP and e.key == K_w:
                player.onGround = True
                up = False
            if e.type == KEYUP and e.key == K_d:
                player.direction = 'right'
                right = False
            if e.type == KEYUP and e.key == K_a:
                player.direction = 'left'
                left = False

        # All of the coin collision detection; when it occurs, the coin is removed and a sound plays while adding one to the coin_count (4 opens the door)
        # the True in each IF statement means that when the collision occurs the coin is removed from it's group, thus removing it from appearing on screen
        if pygame.sprite.spritecollide(player, coinA, True, pygame.sprite.collide_mask):
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(volume)
            coin_list.remove(c1)
            coin_count += 1
        if pygame.sprite.spritecollide(player, coinB, True, pygame.sprite.collide_mask):
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(volume)
            coin_list.remove(c2)
            coin_count += 1
        if pygame.sprite.spritecollide(player, coinC, True, pygame.sprite.collide_mask):
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(volume)
            coin_list.remove(c3)
            coin_count += 1
        if pygame.sprite.spritecollide(player, coinD, True, pygame.sprite.collide_mask):
            sounds.coin_sound.play()
            sounds.coin_sound.set_volume(volume)
            coin_list.remove(c4)
            coin_count += 1

        # If the player manages to reach the trophy, reset the level deaths, add one to the current_level, kill the theme (music), add the loading bar, print out loading level
        #       kill all key-presses (directions) empty all sprites and lists and load in the next level
        if pygame.sprite.spritecollide(player, trophies, True, pygame.sprite.collide_mask):
            deaths = 0
            current_level += 1
            pygame.mixer.music.stop()
            platforms = None
            level = None
            up = False
            right = False
            left = False
            doorA.kill()
            doorB.kill()
            entities.empty()
            trophies.empty()
            spikes.empty()
            coinA.empty()
            coinB.empty()
            coinC.empty()
            coinD.empty()
            screen.blit(loading_bar, (0,0)) # Blit the loading bar image to the screen (so text shows up on all background colors)
            load_text = font.render("Loading Level " + str(current_level) + "...", True, (255, 255, 255)) # Blit loading text to the loading_bar
            screen.blit(load_text, (1,0))
            pygame.display.update()
            gc.collect()
            x = 0
            y = 0
            platforms = []
            pause.sleep(5) # Sleep for 5 seconds ('loading'...might have an effect on lag by allowing it to pause for a few seconds)
            try:
                level = open('levels/level' + str(current_level) + '.txt', 'r') # Try loading the next level; if it fails, we assume they finished the game and reload the title screen
            except:
                screen.blit(loading_bar, (0,0))
                congrats = font.render("Congratulations! You've beaten Master of Thieves!", True, (255, 255, 255))
                screen.blit(congrats, (0,0))
                print "blitted congrats"
                pygame.display.update()
                pause.sleep(5)
                False
                current_level = 0 # Reset the level counter so clicking play again doesn't crash the game
                coin_count = 0 # Reset coin count
                delete_door = True # Reset the door deletion status (True means the door can be removed)
                # Since we're heading back to the title menu, let's bring back the title screen music.
                pygame.mixer.pre_init(44100, -16, 2, 2048)
                sounds = Sounds()
                theme = (Themes(-1)) # Themes(-1) is the theme name within the /sounds/themes folder
                pygame.mixer.music.play(-1, 0.0)
                titleScreen()
            for row in level:
                for col in row:
                    if col == "P":
                        p = Platform(x, y)
                        platforms.insert(0, p)
                        entities.add(p)
                    if col == "C":
                        charX = x
                        charY = y
                        player = Player(charX, charY)
                    if col == "A":
                        spike = Spike(x, y)
                        entities.add(spike)
                        spikes.add(spike)
                    if col == "1":
                        c1 = Coins(x, y)
                        entities.add(c1)
                        coin_list.append(c1)
                        coinA.add(c1)
                    if col == "2":
                        c2 = Coins(x, y)
                        entities.add(c2)
                        coin_list.append(c2)
                        coinB.add(c2)
                    if col == "3":
                        c3 = Coins(x, y)
                        entities.add(c3)
                        coin_list.append(c3)
                        coinC.add(c3)
                    if col == "4":
                        c4 = Coins(x, y)
                        entities.add(c4)
                        coin_list.append(c4)
                        coinD.add(c4)
                    if col == "X":
                        try:
                            win_object = Trophy(x, y, current_level)
                            entities.add(win_object)
                            trophies.add(win_object)
                        except:
                            win_object = Trophy(x, y, 0)
                            entities.add(win_object)
                            trophies.add(win_object)
                    if col == "T":
                        doorA = Door(x, y)
                        platforms.append(doorA)
                        entities.add(doorA)
                    if col == "B":
                        doorB = Door(x, y)
                        platforms.append(doorB)
                        entities.add(doorB)
                    x += 32
                y += 32
                x = 0
            player.update(up, down, left, right, running, platforms)
            for e in entities:
                screen.blit(e.image, camera.apply(e))
            try:
                theme = (Themes(current_level))
                background = pygame.image.load('images/backgrounds/background' + str(current_level) + '.png').convert_alpha() # Try loading the next background and theme; if it fails, use level 0 theme and background
                background_rect = background.get_rect()
            except:
                theme = (Themes(0))
                background = pygame.image.load('images/backgrounds/background0.png').convert_alpha()
                background_rect = background.get_rect()
            pygame.mixer.music.play(-1, 0.0)
            pygame.mixer.music.set_volume(volume)
            pygame.display.update()
            delete_door = True # reset door status
            player.dead = False # ensure the player isn't dead
            coin_count = 0 # reset coin_count
            entities.add(player)

        # Player collision with spike; if true, kill the player
        if pygame.sprite.spritecollide(player, spikes, False, pygame.sprite.collide_mask):
            player.dead = True

        # If the player is dead, reset all key strokes to False, play the death sound, empty all groups and lists and reload the level, add one to both total and level deaths
        if player.dead == True:
            player.onGround = True
            up = False
            right = False
            left = False
            sounds.death_sound.play()
            sounds.death_sound.set_volume(volume)
            player = Player(charX, charY)
            platforms = None
            level = None
            x = 0
            y = 0
            doorA.kill()
            doorB.kill()
            entities.empty()
            trophies.empty()
            spikes.empty()
            coinA.empty()
            coinB.empty()
            coinC.empty()
            coinD.empty()
            gc.collect()
            pause.sleep(1)
            coin_count = 0
            platforms = []
            level = open('levels/level' + str(current_level) + '.txt', 'r')
            deaths += 1
            deaths_total += 1
            for row in level:
                for col in row:
                    if col == "P":
                        p = Platform(x, y)
                        platforms.insert(0, p)
                        entities.add(p)
                    if col == "C":
                        charX = x
                        charY = y
                        player = Player(charX, charY)
                    if col == "A":
                        spike = Spike(x, y)
                        entities.add(spike)
                        spikes.add(spike)
                    if col == "1":
                        c1 = Coins(x, y)
                        entities.add(c1)
                        coin_list.append(c1)
                        coinA.add(c1)
                    if col == "2":
                        c2 = Coins(x, y)
                        entities.add(c2)
                        coin_list.append(c2)
                        coinB.add(c2)
                    if col == "3":
                        c3 = Coins(x, y)
                        entities.add(c3)
                        coin_list.append(c3)
                        coinC.add(c3)
                    if col == "4":
                        c4 = Coins(x, y)
                        entities.add(c4)
                        coin_list.append(c4)
                        coinD.add(c4)
                    if col == "X":
                        win_object = Trophy(x, y, current_level)
                        entities.add(win_object)
                        trophies.add(win_object)
                    if col == "T":
                        doorA = Door(x, y)
                        platforms.append(doorA)
                        entities.add(doorA)
                    if col == "B":
                        doorB = Door(x, y)
                        platforms.append(doorB)
                        entities.add(doorB)
                    x += 32
                y += 32
                x = 0
                delete_door = True
                player.dead = False
            entities.add(player) # Readd the player to the entities

        # If the coin count is four, then set the door status to False, kill the door sprites and remove from the platforms list
        # When delete_door is True it means the door can be removed when the coins are all collected; False means it's been collected. This check was added to prevent it from continually playing the sounds.
        if coin_count >= 4 and delete_door == True:
            sounds.door.play()
            sounds.door.set_volume(volume)
            for x in xrange(2): # Since we ensure doors are added to the end of the list, we can just remove the last two items in the platforms list safely
                del platforms[-1]
            delete_door = False # now the door status is False
            doorA.kill() # Kill doorA and doorB (makes it disappear (the door has "opened"))
            doorB.kill()

        camera.update(player)

        # Update the player and everything else
        player.update(up, down, left, right, running, platforms)
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        pygame.display.update() # Update the display

# Load the title screen to start the game        
titleScreen()