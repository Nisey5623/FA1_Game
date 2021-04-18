#Sprite classes for platform game
import pygame
import math
import random
from Settings import *

vec = pygame.math.Vector2

class Mage(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.health = 3
        self.game = game
        self.walking = False
        self.jumping = True
        self.active_shield = False
        self.last_update = 0
        self.current_frame = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.fire_sound = pygame.mixer.Sound('Fireball_Sound.mp3')

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
class Ability(pygame.sprite.Sprite):
    def __init__(self,x,y,tx,ty,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Mage/Fire_Extra_Update/fire_extra1.png")
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x_wall = Width
        self.y_wall = Height
        self.hit = False
        xdifference = tx - self.rect.centerx
        ydifference = ty - self.rect.centery
        hyp = math.hypot(xdifference,ydifference)
        self.hspeed = xdifference / hyp * speed
        self.vspeed = ydifference / hyp * speed
        angle = (180 / math.pi) * math.atan2(xdifference,ydifference) - 90
        self.image,self.rect = self.rot_center(self.image,self.rect,angle)

    def update(self):
        self.rect.centerx += self.hspeed
        if (self.rect.centerx > self.x_wall) or (self.rect.centerx < 0):
            self.kill()
        self.rect.centery += self.vspeed
        if (self.rect.centery > self.y_wall) or (self.rect.centery < 0):
            self.kill()
        return

    def rot_center(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

class platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Orc(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.idling_frames_r[0]
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False
        self.x_wall = Width
    def load_images(self):
        self.idling_frames_r = [pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_000.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_001.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_002.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_003.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_004.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_005.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_006.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_007.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_008.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_009.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_010.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_011.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_012.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_013.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_014.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_015.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_016.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_017.png"),0,0.10)]
        for frame in self.idling_frames_r:
            frame.set_colorkey(ALPHA)
        self.idling_frames_l = []
        for frame in self.idling_frames_r:
            frame.set_colorkey(ALPHA)
            self.idling_frames_l.append(pygame.transform.flip(frame, True, False))
    def animate_right(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idling_frames_l)
            self.image = self.idling_frames_r[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
    def animate_left(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idling_frames_l)
            self.image = self.idling_frames_l[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
class Caster(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.casting_frames_r[0]
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False

    
    def load_images(self):
        self.casting_frames_r = [pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_000.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_001.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_002.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_003.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_004.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_005.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_006.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_007.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_008.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_009.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_010.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_011.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_012.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_013.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_014.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_015.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_016.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_017.png"),0,0.2)]
        for frame in self.casting_frames_r:
            frame.set_colorkey(ALPHA)
        self.casting_frames_l = []
        for frame in self.casting_frames_r:
            frame.set_colorkey(ALPHA)
            self.casting_frames_l.append(pygame.transform.flip(frame, True, False))

    def animate_right(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.casting_frames_l)
            self.image = self.casting_frames_r[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def animate_left(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.casting_frames_l)
            self.image = self.casting_frames_l[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)        
class Wraith(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.flying_frames_r[0]
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit = False
        self.x_wall = Width
        self.y_wall = Height

    
    def load_images(self):
        self.flying_frames_r = [pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_000.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_001.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_002.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_003.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_004.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_005.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_006.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_007.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_008.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_009.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_010.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_011.png"),0,0.20)]
        for frame in self.flying_frames_r:
            frame.set_colorkey(ALPHA)
        self.flying_frames_l = []
        for frame in self.flying_frames_r:
            frame.set_colorkey(ALPHA)
            self.flying_frames_l.append(pygame.transform.flip(frame, True, False))
        

    def animate_right(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.flying_frames_l)
            self.image = self.flying_frames_r[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
    def animate_left(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.flying_frames_l)
            self.image = self.flying_frames_l[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

class Shield(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotozoom(pygame.image.load('power_up_shield.png'),0,0.35)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collect = True

class Coin(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotozoom(pygame.image.load('Coin.png'),0,0.04)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(White)
        self.rect.x = x
        self.rect.y = y

class Heart(pygame.sprite.Sprite):
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotozoom(pygame.image.load('Heart.png'),0,0.03)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(White)
        self.rect.x = x
        self.rect.y = y
        self.hit = False
    
    def update(self):
        if self.hit == True:
            self.kill()

class Idle_Menu(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Mage/Idle_Edit/idle2.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
