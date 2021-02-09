import pygame
import random
import os,sys
from Settings import *
from sprites import *

#Game Class

class Game:
    def __init__(self): #Initialize game window
        #These two lines initialize the game and the sound for the game.
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        #Creates pygame window, caption and speed monitor.
        self.screen = pygame.display.set_mode((Width, Height))
        pygame.display.set_caption("Tower of Power")
        self.Clock = pygame.time.Clock()
        self.running = True
        

    def new(self): #Start new game
        self.all_sprites = pygame.sprite.Group()
        self.player = Mage()
        self.all_sprites.add(self.player)
        self.run()

    def run(self): #Game Loop
        self.playing = True
        while self.playing:
            self.Clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
    
    def update(self): #Game Loop - Update
        self.all_sprites.update()
    
    def events(self): #Game Loop - Events
        for event in pygame.event.get():
            #Checks if the window is closed to close the window
            if event.type == pygame.QUIT:
                self.playing = False
            self.running = False

    def draw(self): #Game Loop - Draw
        #Fills the screen with the color black    
        #background = pygame.image.load("85850.jpg") 
        #self.screen.blit(background, (0,0)) 
        self.screen.fill(White)
        self.all_sprites.draw(self.screen)
        #The display flip is always last in the game loop.
        pygame.display.flip()

    def show_start_screen(self): #Game Start Screen
        pass

    def show_go_screen(self): #Game End Screen
        pass

ToP = Game()
ToP.show_start_screen()
while ToP.running:
    ToP.new()
    ToP.show_go_screen()

pygame.quit()
sys.exit()