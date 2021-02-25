#Sprite classes for platform game
import pygame
from Settings import *

vec = pygame.math.Vector2

class Mage(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (Width / 2, Height / 2)
        self.pos = vec(Width / 2, Height / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)    

    def load_images(self):
        self.standing_frames = [pygame.image.load("Mage/Idle/idle2.png"), pygame.image.load("Mage/Idle/idle3.png")]
        for frame in self.standing_frames:
            frame.set_colorkey(Black)
        self.walk_frames_r = [pygame.image.load("Mage/Walk/walk1.png"), pygame.image.load("Mage/Walk/walk2.png")]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(Black)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
        self.jump_frame = [pygame.image.load("Mage/Jump/jump1.png"), pygame.image.load("Mage/Jump/jump2.png")]
        


    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -10

    def update(self):
        self.animate()
        self.acc = vec(0,0.8)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
         
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > Width:
            self.pos.x = 0
        if self .pos.x < 0:
            self.pos.x = Width

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                #Fake Comment

class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill(Green)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y