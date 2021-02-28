#Sprite classes for platform game
import pygame
from Settings import *

vec = pygame.math.Vector2

class Mage(pygame.sprite.Sprite):
    def __init__(self,game):
        pygame.sprite.Sprite.__init__(self)
        self.health = 5
        self.game = game
        self.walking = False
        self.jumping = True
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (Width / 2, Height / 2)
        self.pos = vec(Width / 2, Height / 2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)    

    def load_images(self):
        self.standing_frames = [pygame.image.load("Mage/Idle_Edit/idle2.png"), pygame.image.load("Mage/Idle_Edit/idle3.png"), pygame.image.load("Mage/Idle_Edit/idle4.png"), pygame.image.load("Mage/Idle_Edit/idle5.png"), pygame.image.load("Mage/Idle_Edit/idle6.png"), pygame.image.load("Mage/Idle_Edit/idle7.png"), pygame.image.load("Mage/Idle_Edit/idle8.png"), pygame.image.load("Mage/Idle_Edit/idle9.png"), pygame.image.load("Mage/Idle_Edit/idle10.png"), pygame.image.load("Mage/Idle_Edit/idle11.png"), pygame.image.load("Mage/Idle_Edit/idle12.png"), pygame.image.load("Mage/Idle_Edit/idle13.png"), pygame.image.load("Mage/Idle_Edit/idle14.png")]
        for frame in self.standing_frames:
            frame.set_colorkey(Black)
        self.walk_frames_r = [pygame.image.load("Mage/Walk_Edit/walk1.png"), pygame.image.load("Mage/Walk_Edit/walk2.png"), pygame.image.load("Mage/Walk_Edit/walk3.png"), pygame.image.load("Mage/Walk_Edit/walk4.png"), pygame.image.load("Mage/Walk_Edit/walk5.png"), pygame.image.load("Mage/Walk_Edit/walk6.png")]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(Black)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
        self.jump_frame = [pygame.image.load("Mage/Jump/jump1.png"), pygame.image.load("Mage/Jump/jump2.png")]

    def jump(self):
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits:
            print("Yes")
            self.jumping = True
            self.vel.y = -20

    def update(self):
        self.animate()
        self.acc = vec(0,0.7)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
        
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > Width + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = Width + self.rect.width / 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)

class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill(Black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Orc(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = self.idling_frames[0]
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.image = pygame.transform.rotozoom(self.image,0,0.10)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.platforms = pygame.sprite.Group()
        for plat in Platform_list:
            p = platform(*plat)
        self.counter = 0
        self.pos = vec(700,600)
        self.vel = vec(0,0)
        self.acc = vec(0,0)   
    
    def load_images(self):
        self.idling_frames = [pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_000.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_001.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_002.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_003.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_004.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_005.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_006.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_007.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_008.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_009.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_010.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_011.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_012.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_013.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_014.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_015.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_016.png"), pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_017.png")]
        for frame in self.idling_frames:
            frame.set_colorkey(ALPHA)

    def update(self):
        self.acc = vec(0,0.7)
        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
        

class Difficulty(pygame.sprite.Sprite):
    def easy(lvl,eloc):
        if lvl == 1:
            enemy = Orc(eloc[0],eloc[1]) # spawn enemy
            enemy_list = pygame.sprite.Group() # create enemy group
            enemy_list.add(enemy)              # add enemy to group
        if lvl == 2:
            print("Level " + str(lvl) )

        return enemy_list