import pygame
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
        pygame.display.set_caption("Tower of Power")
        self.Clock = pygame.time.Clock()
        #Variable stating that running is true for game loop below
        self.running = True
        
        

    def new(self): #Start new game
        #Creates a sprite group for all sprites and all platforms
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        #Places the player in the centre of the screen and adds player to all_sprites group
        self.player = Mage(self)
        self.all_sprites.add(self.player)
        #Adds the platforms from the platform list to the location while adding them to the two sprite groups
        for plat in Platform_list:
            p = platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        #Runs the game loop from below
        self.run()

    def run(self): #Game Loop
        #Sets the playing variable to while true game updates, checks events and draws
        self.playing = True
        while self.playing:
            self.Clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self): #Game Loop - Update
        #Updates the all_sprites group
        self.all_sprites.update()
        #Checks for collision between player and platform
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
    
    def events(self): #Game Loop - Events
        for event in pygame.event.get():
            #Checks if the window is closed to close the game window
            if event.type == pygame.QUIT:
                self.playing = False
            self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def draw(self): #Game Loop - Draw  
        #background = pygame.image.load("85850.jpg") 
        #self.screen.blit(background, (0,0)) 
        #Sets a white screen
        self.screen.fill(White)
        #Draws the all_sprites group
        self.all_sprites.draw(self.screen)
        #The display flip is always last in the game loop.
        pygame.display.flip()

    def show_start_screen(self): #Game Start Screen
        pass

    def show_go_screen(self): #Game End Screen
        pass

ToP = Game()
ToP.show_start_screen()
#While running variable is equal to true the game runs and quits when closed
while ToP.running:
    ToP.new()
    ToP.show_go_screen()

pygame.quit()
sys.exit()