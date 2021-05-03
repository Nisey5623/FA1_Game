import pygame
import math
import random
from Settings import *

#Utilised vector math for hypotenuse calculations
vec = pygame.math.Vector2

class Mage(pygame.sprite.Sprite): #Player sprite
    def __init__(self,game,x,y): #Sprite initialization
        pygame.sprite.Sprite.__init__(self)
        #All variables used for the player are defined in the __init__
        self.health = 3
        self.game = game
        self.walking = False
        self.jumping = True
        self.active_shield = False
        self.last_update = 0
        self.current_frame = 0
        self.load_images()
        #Sets the image for the sprite using the first image from the list
        self.image = self.standing_frames[0]
        
        #Uses the image to determine the rect of the player
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        #Maths velocity, acceleration and position of the player
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        #Sound effect of ability
        self.fire_sound = pygame.mixer.Sound('Fireball_Sound.mp3')

    def load_images(self): #Load images function
        #List of all sprite frames used when moving or idling
        self.standing_frames = [pygame.image.load("Mage/Idle_Edit/idle2.png"), pygame.image.load("Mage/Idle_Edit/idle3.png"), pygame.image.load("Mage/Idle_Edit/idle4.png"), pygame.image.load("Mage/Idle_Edit/idle5.png"), pygame.image.load("Mage/Idle_Edit/idle6.png"), pygame.image.load("Mage/Idle_Edit/idle7.png"), pygame.image.load("Mage/Idle_Edit/idle8.png"), pygame.image.load("Mage/Idle_Edit/idle9.png"), pygame.image.load("Mage/Idle_Edit/idle10.png"), pygame.image.load("Mage/Idle_Edit/idle11.png"), pygame.image.load("Mage/Idle_Edit/idle12.png"), pygame.image.load("Mage/Idle_Edit/idle13.png"), pygame.image.load("Mage/Idle_Edit/idle14.png")]
        self.walk_frames_r = [pygame.image.load("Mage/Walk_Edit/walk1.png"), pygame.image.load("Mage/Walk_Edit/walk2.png"), pygame.image.load("Mage/Walk_Edit/walk3.png"), pygame.image.load("Mage/Walk_Edit/walk4.png"), pygame.image.load("Mage/Walk_Edit/walk5.png"), pygame.image.load("Mage/Walk_Edit/walk6.png")]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            #Flips frame of sprite horizontally and not vertically
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))

    def jump(self): #Jump function when space bar pressed
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        #If player hits platform then changes velocity
        if hits:
            self.jumping = True
            self.vel.y = -20

    def update(self): #Update of player sprite
        #Animates the player every update
        self.animate()

        #Gravity is defined by 0.7 acceleration pushing the player down
        self.acc = vec(0,0.7)

        #If a or left key pressed then x acceleration is subtracted by player acceleration
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.acc.x = -PLAYER_ACC

        #If d or right key pressed then x acceleration is added by player acceleration
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        
        #Player friction is defined to stop infinite acceleration
        self.acc.x += self.vel.x * PLAYER_FRICTION

        #Velocity is added based on acceleration
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        #Position is updated based on the player's velocity and acceleration values
        self.pos += self.vel + 0.5 * self.acc

        #Wraps the player around the screen
        if self.pos.x > Width + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = Width + self.rect.width / 2
        
        #The player's rect value is the player's position
        self.rect.midbottom = self.pos

    def animate(self): #Animate function of player
        #Ticks since game run and updated
        now = pygame.time.get_ticks()
        #Checks if the player is walking based on the player's velocity and sets walking variable accordingly
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        #If the player is walking then the frame updates to the next frame every update
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

        #Checks if the player is jumping or walking to animate the idling frames
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        #Sets the sprite's surface mask
        self.mask = pygame.mask.from_surface(self.image)
class Ability(pygame.sprite.Sprite): #Ability function
    def __init__(self,x,y,tx,ty,speed):
        pygame.sprite.Sprite.__init__(self)
        #Sets the image of the sprite and sets its rect based on the image
        self.image = pygame.image.load("Mage/Fire_Extra_Update/fire_extra1.png")
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        #Sets the walls of the screen
        self.x_wall = Width
        self.y_wall = Height
        
        #Creates the difference between the targets coordinates and its rect
        xdifference = tx - self.rect.centerx
        ydifference = ty - self.rect.centery
        
        #Creates a hypotenuse as the sprite path use x and y difference
        hyp = math.hypot(xdifference,ydifference)

        #Sets the horizontal and vertical speed of the sprite based on x and y difference
        self.hspeed = xdifference / hyp * speed
        self.vspeed = ydifference / hyp * speed

        #Sets the angle of the fireball based on where the target is
        angle = (180 / math.pi) * math.atan2(xdifference,ydifference) - 90

        #Rotates the sprite based on the image, rect and angle
        self.image,self.rect = self.rot_center(self.image,self.rect,angle)

    def update(self): #Sprite update function
        #Updates the ability x and y coordinates based on hspeed and vspeed
        self.rect.centerx += self.hspeed
        if (self.rect.centerx > self.x_wall) or (self.rect.centerx < 0):
            self.kill()
        self.rect.centery += self.vspeed
        if (self.rect.centery > self.y_wall) or (self.rect.centery < 0):
            self.kill()
        return

    def rot_center(self, image, rect, angle): #Rotates the sprite absed on angle, rect and image
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect

class platform(pygame.sprite.Sprite): #Platform class
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        #Sets the image and rect of the platform class
        self.image = pygame.transform.rotozoom(pygame.image.load("Leaves.png"),0,0.75)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class nonplatform(pygame.sprite.Sprite): #Invisible platform class
    def __init__(self, x, y, w, h,color):
        pygame.sprite.Sprite.__init__(self)
        #Sets the image and rect of the platform class
        self.image = pygame.Surface((w,h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
class Orc(pygame.sprite.Sprite): #Orc enemy class
    def __init__(self,game,x,y,):
        pygame.sprite.Sprite.__init__(self)
        #Initialises the variables of the orc class including image, rect and others for animation
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
    def load_images(self): #Load images for animation by frames
        self.idling_frames_r = [pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_000.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_001.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_002.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_003.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_004.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_005.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_006.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_007.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_008.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_009.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_010.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_011.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_012.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_013.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_014.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_015.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_016.png"),0,0.10), pygame.transform.rotozoom(pygame.image.load("Orc/Idle Blinking_Edit/0_Orc_Idle Blinking_017.png"),0,0.10)]
        for frame in self.idling_frames_r:
            frame.set_colorkey(ALPHA)
        self.idling_frames_l = []
        for frame in self.idling_frames_r:
            frame.set_colorkey(ALPHA)
            self.idling_frames_l.append(pygame.transform.flip(frame, True, False))
    def animate_right(self): #Animates the orc when tracking player to the right
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idling_frames_l)
            self.image = self.idling_frames_r[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
    def animate_left(self): #Animates the orc when tracking player to the left
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idling_frames_l)
            self.image = self.idling_frames_l[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
class Caster(pygame.sprite.Sprite): #Caster enemy class
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Creates variables required for class including the rect, image and others
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.casting_frames_r[0]
        self.image.convert_alpha()
        self.image.set_colorkey(ALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.hit = False

    def load_images(self): #Loading images per frame for animation
        self.casting_frames_r = [pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_000.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_001.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_002.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_003.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_004.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_005.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_006.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_007.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_008.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_009.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_010.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_011.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_012.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_013.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_014.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_015.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_016.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Cyan Wraith/Casting_Spells_Edit/Wraith_01_Casting Spells_017.png"),0,0.2)]
        for frame in self.casting_frames_r:
            frame.set_colorkey(ALPHA)
        self.casting_frames_l = []
        for frame in self.casting_frames_r:
            frame.set_colorkey(ALPHA)
            self.casting_frames_l.append(pygame.transform.flip(frame, True, False))

    def animate_right(self): #Animates the sprite to the right
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.casting_frames_l)
            self.image = self.casting_frames_r[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def animate_left(self): #Animates the sprite to the left
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.casting_frames_l)
            self.image = self.casting_frames_l[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)        
class Wraith(pygame.sprite.Sprite): #Wraith enemy class
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Creates variable required for the enemy sprite, image, rect and positions of the x and y wall of screen
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

    
    def load_images(self): #Loads frame of images required for animation
        self.flying_frames_r = [pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_000.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_001.png"),0,0.2), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_002.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_003.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_004.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_005.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_006.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_007.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_008.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_009.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_010.png"),0,0.20), pygame.transform.rotozoom(pygame.image.load("Purple Wraith/Attacking_Edit/Wraith_03_Attack_011.png"),0,0.20)]
        for frame in self.flying_frames_r:
            frame.set_colorkey(ALPHA)
        self.flying_frames_l = []
        for frame in self.flying_frames_r:
            frame.set_colorkey(ALPHA)
            self.flying_frames_l.append(pygame.transform.flip(frame, True, False))
        

    def animate_right(self): #Animates sprite to the right
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.flying_frames_l)
            self.image = self.flying_frames_r[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
    def animate_left(self): #Animates sprite to the left
        now = pygame.time.get_ticks()
        if now - self.last_update > 180:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.flying_frames_l)
            self.image = self.flying_frames_l[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

class Shield(pygame.sprite.Sprite): #Shield sprite
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Variables from image, rect and collect
        self.image = pygame.transform.rotozoom(pygame.image.load('power_up_shield.png'),0,0.35)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collect = True

class Coin(pygame.sprite.Sprite): #Coin sprite for main menu and game screen
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Sets image and rect
        self.image = pygame.transform.rotozoom(pygame.image.load('Coin.png'),0,0.04)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(White)
        self.rect.x = x
        self.rect.y = y

class Heart(pygame.sprite.Sprite): #Heart sprite for main menu and game screen
    def __init__(self,game,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Sets image and rect
        self.image = pygame.transform.rotozoom(pygame.image.load('Heart.png'),0,0.03)
        self.rect = self.image.get_rect()
        self.image.set_colorkey(White)
        self.rect.x = x
        self.rect.y = y
        self.hit = False
    
    def update(self): #Update function for heart sprite
        if self.hit == True:
            self.kill()

class Idle_Menu(pygame.sprite.Sprite): #Idle player sprite for main menu
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #Creates image and rect
        self.image = pygame.image.load("Mage/Idle_Edit/idle2.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  