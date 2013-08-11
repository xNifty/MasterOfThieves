import pygame
from pygame.locals import *
from entities import *

class Player(Entity):
    def __init__(self, x, y):
        """The player class handles all actions of the user. It is the C in level loading."""
        Entity.__init__(self)
        self.xvel = 0
        self.yvel = 0
        self.dead = False
        self.direction = 'right'
        self.onGround = True
        self.canDie = True
        self.coin_count = 0
        self.image = pygame.transform.scale(pygame.image.load("images/Thief.png"), (40, 40))
        self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(x, y, 32, 40)

    def update(self, up, down, left, right, platforms):
        """Handle the directions of the character and change the image based on left or right."""
        if up:
            # only jump if on the ground
            if self.onGround: 
                self.yvel -= 10
        if left and self.dead == False:
            self.direction = 'left'
            self.image = pygame.transform.scale(pygame.image.load("images/Thief2.png"), (40, 40))
            self.image.convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.xvel = -8
        if right and self.dead == False:
            self.direction = 'right'
            self.image = pygame.transform.scale(pygame.image.load("images/Thief.png"), (40, 40))
            self.image.convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.xvel = 8
        if self.onGround == False:
            # only accelerate with gravity if in the air
            self.yvel += 0.95
            # max falling speed
            if self.yvel > 100: self.yvel = 100
        if not(left or right):
            self.xvel = 0

        # increment in x direction
        self.rect.left += self.xvel

        # do x-axis collisions
        self.collide(self.xvel, 0, platforms)

        # increment in y direction
        self.rect.top += self.yvel

        # assuming we're in the air
        self.onGround = False;

        # do y-axis collisions
        self.collide(0, self.yvel, platforms)


    def collide(self, xvel, yvel, platforms):
        """Handles collisions with platforms."""
        for p in platforms:
            if self.rect.colliderect(p):
            #if pygame.sprite.collide_mask(self, p):
                if xvel > 0:
                    self.rect.right = p.rect.left
                if xvel < 0:
                    self.rect.left = p.rect.right
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

    def getStatus(self):
        return self.dead

    def getCoins(self):
        return self.coin_count

    def setCoins(self):
        self.coin_count = 4

    def addCoin(self):
        self.coin_count += 1

    def resetCoins(self):
        self.coin_count == 0