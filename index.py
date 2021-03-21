import pygame
import pygame_menu
import random
import os,sys
from Settings import *
from sprites import *

#Game Class

class Game:
    def __init__(self): #Initialize game window
        #These three lines initialize the game, sound and font for the game.
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        #Creates pygame window, caption and speed monitor.
        self.screen = pygame.display.set_mode((Width, Height))
        self.myfont = pygame.font.SysFont('Calibri', 30)
        pygame.display.set_caption("Tower of Power")
        self.Clock = pygame.time.Clock()
        #Variable stating that running is true for game loop below
        self.running = True
        self.shooting = True
        
        

    def new(self): #Start new game
        #Creates a sprite group for all sprites and all platforms
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        #Places the player in the scentre of the screen and adds player to all_sprites group
        self.player = Mage(self)
        self.enemy = Orc(self,400,668)
        self.wraith = Wraith(self,300,300)
        self.caster = Caster(self,800,150)
        self.enemy_list = pygame.sprite.Group()
        self.enemy_list.add(self.enemy)
        self.enemy_list.add(self.caster)
        self.enemy_list.add(self.wraith)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player)
        self.wraithupdate = True
        self.hit = False
        #Adds the platforms from the platform list to the location while adding them to the two sprite groups
        for plat in Platform_list:
            p = platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        #Runs the game loop from below
        self.run()
        return

    def run(self): #Game Loop
        #Sets the playing variable to while true game updates, checks events and draws while playing is true
        self.playing = True
        while self.playing:
            self.Clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self): #Game Loop - Update
        #Updates the all_sprites group
        self.all_sprites.update()
        self.enemy_list.update()
        self.fireballs.update()
        if self.caster.casting_frames_l[17]:
            enemy_fire = Ability(self.caster.rect.x,self.caster.rect.y,self.player.rect.x,self.player.rect.y)
        Orcxdifference = self.player.rect.x - self.enemy.rect.x
        Wraithxdifference = self.player.rect.x - self.wraith.rect.x
        Wraithydifference = self.player.rect.x - self.wraith.rect.x
        #hyp = math.hypot(xdifference)
        if Orcxdifference != 0:
            self.orchspeed = (Orcxdifference / Orcxdifference * 3)
            if Orcxdifference > 800:
                self.orchspeed = 0
        else:
            self.orchspeed = 0
        if self.player.rect.x < self.enemy.rect.x:
            self.enemy.rect.x -= self.orchspeed
            self.enemy.animate_left()
        if self.player.rect.x > self.enemy.rect.x:
            self.enemy.rect.x += self.orchspeed 
            self.enemy.animate_right()
        if self.player.rect.x < self.caster.rect.x:
            self.caster.animate_left()
        if self.player.rect.x > self.caster.rect.x:
            self.caster.animate_right()
        if Wraithxdifference != 0 and Wraithydifference != 0:
            self.wraithhspeed = (Wraithxdifference / Wraithxdifference * 2.5)
            self.wraithvspeed = (Wraithydifference / Wraithydifference * 2.5)
        else:
            self.wraithhspeed = 0
            self.wraithvspeed = 0
        if self.player.rect.x < self.wraith.rect.x:
            self.wraith.rect.x -= self.wraithhspeed
            self.wraith.animate_left()
        if self.player.rect.x > self.wraith.rect.x:
            self.wraith.rect.x += self.wraithhspeed 
            self.wraith.animate_right()
        if self.wraithupdate:                
            if self.player.rect.y < self.wraith.rect.y:
                self.wraith.rect.y -= self.wraithvspeed
            if self.player.rect.y > self.wraith.rect.y:
                self.wraith.rect.y += self.wraithvspeed 
            self.wraithupdate = False
            pygame.time.set_timer(pygame.USEREVENT + 2, 25)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0):
            if self.shooting:
                self.fire = Ability(self.player.pos.x,self.player.pos.y-30, mouse_x, mouse_y)
                self.fireballs.add(self.fire)
                self.shooting = False
                pygame.time.set_timer(pygame.USEREVENT + 1, 500)
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.jumping = False
        if self.hit == False:
            hit_list = pygame.sprite.spritecollide(self.player, self.enemy_list, False)
            for enemy in hit_list:
                if self.enemy.hit == False:
                    self.player.health -= 1
                    self.enemy.hit = False
                    self.player.pos.x += 50
                    self.hit = True
                    pygame.time.set_timer(pygame.USEREVENT + 3, 2000)
                    timer = 2000 - int(pygame.time.get_ticks()/1000)
                    timer = str(timer)
                    self.hit_timer = self.myfont.render("Time: " + timer,True,(255,255,255))
                    self.screen.blit(self.hit_timer,(self.player.pos.x,self.player.pos.y + 50))

                
                #print(self.player.health)
                #if timer > 3:
                    #self.enemy.hit = False
        fire_enemy_hit = pygame.sprite.groupcollide(self.enemy_list,self.fireballs, True, True)
        fire_plat_hit = pygame.sprite.groupcollide(self.fireballs,self.platforms, True, False)
        
        
        #Check for scrolling
        if self.player.rect.right >= (Width - (Width / 4)):
            self.player.pos.x -= abs(self.player.vel.x) 
            for plat in self.platforms:
                plat.rect.x -= abs(self.player.vel.x)   
            for e in self.enemy_list:
                e.rect.x -= abs(self.player.vel.x)
        if self.player.rect.left <= Width / 4:
            self.player.pos.x += abs(self.player.vel.x) 
            for plat in self.platforms:
                plat.rect.x += abs(self.player.vel.x)
            for e in self.enemy_list:
                e.rect.x += abs(self.player.vel.x)
    
    def events(self): #Game Loop - Events
        for event in pygame.event.get():
            #Checks if the window is closed to close the game window
            if event.type == pygame.QUIT:
                self.playing = False
            self.running = False
            if event.type == pygame.USEREVENT + 1:
                self.shooting = True
                pygame.time.set_timer(pygame.USEREVENT + 1,0)
            if event.type == pygame.USEREVENT + 2:
                self.wraithupdate = True
                pygame.time.set_timer(pygame.USEREVENT + 2, 0)
            if event.type == pygame.USEREVENT + 3:
                self.hit = False
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self): #Game zLoop - Draw  
        background = pygame.image.load("Temple Background.jpg") 
        self.screen.blit(background, (0,0))
        
        #Sets a blue screen
        #self.screen.fill(Blue)
        #Draws the all_sprites group
        self.enemy_list.draw(self.screen)
        self.fireballs.draw(self.screen)
        #pygame.draw.rect(self.screen, Red, self.player.rect)
        #pygame.draw.rect(self.screen, Red, self.enemy.rect)
        #for e in self.enemy_list:
            #e.move()
        self.all_sprites.draw(self.screen)
        #The display flip is always last in the game loop.
        pygame.display.flip()

    def show_start_screen(self): #Game Start Screen
        menu = pygame_menu.Menu(300,400,'Marlin the Mage', theme=pygame_menu.themes.THEME_BLUE)
        menu.add_button('Play',self.new)
        menu.add_button('Shop', pygame_menu.events.EXIT)
        menu.add_button('Times', pygame_menu.events.EXIT)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)

    def show_go_screen(self): #Game End Screen
        pass

MtM = Game()
MtM.show_start_screen()
#While running variable is equal to true the game runs and quits when closed
while MtM.running:
    MtM.new()
    MtM.show_go_screen()

pygame.quit()
sys.exit()