#Sprite classes for platform game
import pygame
from Settings import *

vec = pygame.math.Vector2

class Mage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30,40))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.center = (Width / 2, Height / 2)
        self.pos = vec(Width / 2, Height / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)    

    def update(self):
        self.acc = vec(0,0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
         
        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > Width:
            self.pos.x = 0
        if self .pos.x < 0:
            self.pos.x = Width

        self.rect.center = self.pos