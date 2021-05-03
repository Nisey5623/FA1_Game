import pygame
import random
import os,sys
from Settings import *
from sprites import *
import ptext
class Game:
    def __init__(self): #Initialize game window
        #These three lines initialize the game, sound and font for the game.
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        #Creates pygame window, caption and speed monitor.
        self.screen = pygame.display.set_mode((Width, Height))
        self.font_name = pygame.font.match_font('Calibri')
        self.myfont = pygame.font.SysFont('Calibri', 30)
        pygame.display.set_caption("Marlin the Mage")
        self.Clock = pygame.time.Clock()

        #Upon game starting the menu music begins
        self.menu_music = True

        #Variable stating that running is true for game loop below
        self.running = True
        
        #Player and enemy can shoot upon spawning
        self.shooting = True
        self.enemy_shooting = True

        #File location for times storing
        self.filename = 'times.txt'

        #Number of enemies per room, starts at zero before level begins
        self.enemies = 0

        #Volume set at full for initialization
        pygame.mixer.music.set_volume(1)
        self.volume = pygame.mixer.music.get_volume()

        #Upon level begin the enemies are delayed
        self.game_delay = True

        #First level begins at the tutorial
        self.level = 0
        self.played_level = 0
        self.latest_level = 0
        self.highest_level = 0

        #Coins held during game
        self.coins = 0

        #Mode of game at the beginning with multiplier for number of enemies
        self.mode = 'Easy Mode'
        self.multiplier = 1

        #Levels background
        self.background = pygame.image.load("sized_background.jpg")

        #Other variables being stated, including tutorial for level 0
        self.heart_loss = False
        self.tutorial_mode_1 = True
        self.tutorial_mode_2 = False
        self.tutorial_mode_3 = False
        self.health = 3
        self.extra_health = 0

        #All groups created
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.enemy_fireballs = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.orc_list = pygame.sprite.Group()
        self.wraith_list = pygame.sprite.Group()
        self.caster_list = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        self.hearts = pygame.sprite.Group()   

    def new(self): #Start new game
        #Loads music upon level running
        pygame.mixer.music.load('Temple Run (iOS) Music- Running Music (128 kbps).mp3') 
        self.menu_music = True

        #Sets enemy number in room to 0
        self.enemies = 0

        #Spawns the player in middle of the room on bottom platform and adds to group
        self.player = Mage(self,Width/2,668)
        self.players.add(self.player)

        #Health of player at the start of the level
        self.health = 3 + self.extra_health
        
        #Spawns the shield powerup and adds to group
        self.shield = Shield(self,random.randint(100,900),random.randint(500,640))
        self.power_ups.add(self.shield)

        #Adds coin label at top left corner
        self.coin = Coin(self,50,25)
        self.all_sprites.add(self.coin)
        
        #Sets the mode of the level and determines the multiplier for the enemies number
        if self.mode == 'Easy Mode':
            self.active_color = Menu_Red
            self.inactive_color = Inactive_Menu_Red
            self.multiplier = 1
        if self.mode == 'Hard Mode':
            self.tutorial_mode_1 = False
            self.tutorial_mode_2 = False
            self.tutorial_mode_3 = False
            self.active_color = Menu_Green
            self.inactive_color = Inactive_Menu_Green
            self.multiplier = 2
        if self.mode == 'Master Mode':
            self.tutorial_mode_1 = False
            self.tutorial_mode_2 = False
            self.tutorial_mode_3 = False
            self.active_color = Menu_Blue
            self.inactive_color = Inactive_Menu_Blue
            self.multiplier = 3

        #Creates hearts for health amount of player
        add = 0
        for i in range(self.health):
            self.hearts.add(Heart(self,50+add,90))
            add += 35
        self.all_sprites.add(self.hearts)

        #Determines the number of enemies to spawn based on what level is being played
        if self.level == 0:
            enemy_number = 1 * self.multiplier
            wraith_number = 1 * self.multiplier
            caster_number = 1 * self.multiplier
            self.played_level = 0
        if self.level == 1:
            enemy_number = random.randint(1,2) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = 1 * self.multiplier
            self.tutorial_mode_1 = False
            self.played_level = 1
        if self.level == 2:
            enemy_number = random.randint(1,3) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
            self.tutorial_mode_1 = False
            self.played_level = 2
        if self.level == 3:
            enemy_number = random.randint(1,2) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = 1 * self.multiplier
            self.tutorial_mode_1 = False
            self.played_level = 3
        if self.level == 4:
            enemy_number = random.randint(1,3) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
            self.tutorial_mode_1 = False
            self.played_level = 4
        if self.level == 5:
            enemy_number = random.randint(2,3) * self.multiplier
            wraith_number = random.randint(1,3) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
            self.tutorial_mode_1 = False
            self.played_level = 5
        if self.level == 6:
            enemy_number = random.randint(2,3) * self.multiplier
            wraith_number = random.randint(2,3) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
            self.tutorial_mode_1 = False
            self.played_level = 6
        if self.level == 7:
            enemy_number = random.randint(3,4) * self.multiplier
            wraith_number = 3 * self.multiplier
            caster_number = 3 * self.multiplier
            self.tutorial_mode_1 = False
            self.played_level = 7

        #Spawns the enemies in random locations based on the enemy type and adds to the enemies group
        for i in range(0,enemy_number):
            self.orc_list.add(Orc(self,random.randint(100,1000),608))
            self.enemies += 1
        for i in range(0,wraith_number):
            self.wraith_list.add(Wraith(self,random.randint(100,1000),random.randint(200,400)))
            self.enemies += 1
        position = [(169,341),(160,479),(374,443),(376,261),(815,305),(810,475)]
        for i in range(0,caster_number):
            the_position = random.randint(0,5)
            self.caster_list.add(Caster(self,*position[the_position]))
            self.enemies += 1
        self.enemy_list.add(self.orc_list)
        self.enemy_list.add(self.caster_list)
        self.enemy_list.add(self.wraith_list)
        self.all_sprites.add(self.player)
        self.wraithupdate = True
        self.hit = False

        #Spawns the platform at the bottom of screen
        Platform_non_list = [(0,667,1100,40,Black)]
        for plat in Platform_non_list:
            p = nonplatform(*plat)
            self.platforms.add(p)

        #Randomly chooses the location for the leaves block and adds to group
        Platform_see_list = [((Width/5)-30,501,100,20),((Width/5) + (Width/5)-30,501,40,20),((Width/5) + (Width/5) + (Width/5)-30,501,40,20),((Width/5) + (Width/5) + (Width/5) + (Width/5)-30,501,40,20)]
        leaves = random.randint(0,3)
        p = platform(*Platform_see_list[leaves])
        self.all_sprites.add(p)
        self.platforms.add(p)

        #Sets the game times to zero in preparation of game start
        self.game_seconds = 0
        self.game_minutes = 0 
        self.counts = 0

        #Runs the game loop from below
        self.run()    

        return

    def run(self): #Game Loop
        #Sets the playing variable to true while game updates, checks events and draws while playing is true and plays music
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.Clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            if self.tutorial_mode_1 == True:
                self.tutorial_1()
            if self.tutorial_mode_2 == True:
                self.tutorial_2()
            if self.tutorial_mode_3 == True:
                self.tutorial_3()
                self.tutorial_mode_3 = False
        pygame.mixer.music.fadeout(1000)
        return
    
    def update(self): #Game Loop - Update
        #Per frame the total seconds increases based on frames loaded
        self.total_seconds = self.counts // FPS
        self.game_minutes = self.total_seconds // 60
        self.game_seconds = self.total_seconds % 60
        self.counts += 1

        #Kills the player if game minutes is more than five to stop computer overloading
        if self.game_minutes > 5:
            self.player.kill()
            self.enemy_list.empty()
            self.game_over_screen()

        #Adds the coins label to top left of screen
        self.coins = str(self.coins)
        self.label = self.myfont.render(self.coins,True,White)

        #Updates all sprite groups
        self.all_sprites.update()
        self.enemy_list.update()
        self.enemy_fireballs.update()
        self.fireballs.update()
        self.power_ups.update()

        #Stops the enemies updating until game delay is over
        if self.game_seconds > 0.5:

            #Sets the animation and tracking of the Orc based on the x difference between player and Orc
            for i in self.orc_list:
                self.Orcxdifference = self.player.rect.x - i.rect.x
                if self.Orcxdifference != 0:
                    self.orchspeed = (self.Orcxdifference / self.Orcxdifference * random.randint(1,5))
                else:
                    self.orchspeed = 0
                if self.player.rect.x < i.rect.x:
                    i.rect.x -= self.orchspeed
                    i.animate_left()
                if self.player.rect.x > i.rect.x:
                    i.rect.x += self.orchspeed 
                    i.animate_right()

            #Sets the animation and tracking of the Wraith based on x and y difference using hypotenuse calculations to move towards player
            for w in self.wraith_list:
                Wraithxdifference = self.player.rect.x - w.rect.x
                Wraithydifference = self.player.rect.y - w.rect.y
                if Wraithxdifference != 0:
                    self.wraithhspeed = (Wraithxdifference / Wraithxdifference * random.randint(2,4))
                else:
                    self.wraithhspeed = 0
                if Wraithydifference != 0:
                    self.wraithvspeed = (Wraithydifference / Wraithydifference * random.randint(2,4))
                else:
                    self.wraithvspeed = 0
                if self.player.rect.x < w.rect.x:
                    w.rect.x -= self.wraithhspeed
                    w.animate_left()
                elif self.player.rect.x > w.rect.x:
                    w.rect.x += self.wraithhspeed 
                    w.animate_right()  
                if self.player.rect.y < w.rect.y:
                    w.rect.y -= self.wraithvspeed
                elif self.player.rect.y > w.rect.y:
                    w.rect.y += self.wraithvspeed 

            #Sets the animation of the Caster enemy, tells the enemy when to shoot at player and which direction the player is in
            for c in self.caster_list:
                if c.current_frame == 17 or c.current_frame == 9:
                    if self.enemy_shooting:
                        enemy_fire = Ability(c.rect.x,c.rect.y,self.player.pos.x,self.player.pos.y,8)
                        self.enemy_fireballs.add(enemy_fire)
                        self.enemy_shooting = False
                        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
                if self.player.rect.x < c.rect.x:
                    c.animate_left()
                if self.player.rect.x > c.rect.x:
                    c.animate_right()

        #Empties all sprite groups if player has no health
        if self.health <= 0:
            self.enemy_list.empty()
            self.players.empty()
            self.orc_list.empty()
            self.wraith_list.empty()
            self.caster_list.empty()
            self.all_sprites.empty()
            self.fireballs.empty()
            self.enemy_fireballs.empty()
            self.power_ups.empty()
            self.platforms.empty()
            self.hearts.empty()
            self.player.kill()
            self.game_over_screen()
        self.sprite_collisions()
    
    def sprite_collisions(self): #All sprite groups collisions
        #Based on the rects of a sprite in its sprite group the spritecollide function determines the collisions

        #Tracks the position of the mouse and when left click is used the ability moves towards the mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0):
            if self.shooting:
                self.fire = Ability(self.player.pos.x,self.player.pos.y-30, mouse_x, mouse_y,10)
                self.fireballs.add(self.fire)
                self.player.fire_sound.set_volume(self.volume)
                self.player.fire_sound.play()
                self.shooting = False
                pygame.time.set_timer(pygame.USEREVENT + 1, 400)

        #Checks for collisions between player and platform
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.jumping = False

        #Checks for collisions between enemies in enemy list and the player sprite, removes player life if collision, checks if shield is active
        if self.hit == False:
            if self.player.active_shield == False:
                hit_list = pygame.sprite.spritecollide(self.player, self.enemy_list, False)
                for enemy in hit_list:
                    if enemy.hit == False:
                        self.health -= 1
                        self.heart_loss = True
                        for heart in self.hearts:
                            if self.heart_loss == True:
                                heart.hit = True
                                self.heart_loss = False
                                self.heart_timer = pygame.time.set_timer(pygame.USEREVENT + 5, 2000)
                        enemy.hit = False
                        self.player.pos.x = Width / 2
                        self.player.pos.y = Height / 2
                        self.hit = True
                        self.timer = pygame.time.set_timer(pygame.USEREVENT + 3, 2000)

        #Checks for collision between player and enemies fireball
        if self.player.active_shield == False:
            enemyfire_hit = pygame.sprite.spritecollide(self.player,self.enemy_fireballs,False)
            if enemyfire_hit:
                self.health -= 1

        #Checks for collision between player fireball and enemies, deletes both if collision is true
        fire_enemy_hit = pygame.sprite.groupcollide(self.enemy_list,self.fireballs, True, True)
        for i in fire_enemy_hit:
            self.enemies -= 1
            self.coins = int(self.coins)
            self.coins += 10
        
        #Checks for collisions between the enemy fireballs group and the platforms group
        fire_plat_hit = pygame.sprite.groupcollide(self.enemy_fireballs,self.platforms, True, False)

        #Checks for collision between the player and the powerups group
        if self.shield.collect == True:
            shield_activate = pygame.sprite.groupcollide(self.players,self.power_ups,False,False)
            if shield_activate:
                self.shield.rect.x = 45
                self.shield.rect.y = 52
                self.player.active_shield = True
                self.shield.collect = False
                pygame.time.set_timer(pygame.USEREVENT + 4, 5000)

        #Checks if the room has zero enemies and will therefore empty all lists and move to win screen
        if self.enemies <= 0:
            self.times_add()
            self.enemy_list.empty()
            self.players.empty()
            self.orc_list.empty()
            self.wraith_list.empty()
            self.caster_list.empty()
            self.all_sprites.empty()
            self.fireballs.empty()
            self.enemy_fireballs.empty()
            self.power_ups.empty()
            self.platforms.empty()
            self.hearts.empty()
            self.player.kill()
            self.latest_level += 1
            self.coins += 50

            #Checks if level seven was complete, if so changes the mode
            if self.latest_level > 7:
                if self.mode == 'Easy Mode':
                    self.mode = 'Hard Mode'
                else:   
                    self.mode = 'Master Mode'
            self.win_screen()

    def events(self): #Game Loop - Events
        for event in pygame.event.get():

            #Checks if the window is closed to close the game window
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()

            #Checks if the first timer is complete and sets the shooting variable to true
            if event.type == pygame.USEREVENT + 1:
                self.shooting = True
                pygame.time.set_timer(pygame.USEREVENT + 1,0)

            #Checks if the second timer is complete, and sets enemy shooting to true
            elif event.type == pygame.USEREVENT + 2:
                self.enemy_shooting = True
                pygame.time.set_timer(pygame.USEREVENT + 2,0)

            #Chekcs if the third timer is complete, sets the hit variable to false
            elif event.type == pygame.USEREVENT + 3:
                self.hit = False
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)

            #Checks if the fourth timer is complete, sets the active shield variable to false and the shield collect to true
            elif event.type == pygame.USEREVENT + 4:
                self.player.active_shield = False
                self.shield.collect = True
                self.shield.kill()
                pygame.time.set_timer(pygame.USEREVENT + 4, 0)
            
            #Checks if the fifth timer is complete, sets the heart loss variable to false
            elif event.type == pygame.USEREVENT + 5:
                self.heart_loss = False
                pygame.time.set_timer(pygame.USEREVENT + 5, 0)

            #Checks if the sixth and seventh timers are complete, sets the tutorial modes to true
            elif event.type == pygame.USEREVENT + 6:
                self.tutorial_mode_2 = True
                pygame.time.set_timer(pygame.USEREVENT + 6, 0)
            elif event.type == pygame.USEREVENT + 7:
                self.tutorial_mode_3 = True
                pygame.time.set_timer(pygame.USEREVENT + 7, 0)
            
            #Checks if the space key is being pressed and activates the player jump, if escape key pressed, pause menu shows
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.pause_menu()
        return

    def draw(self): #Game Loop - Draw  
        #All sprite groups and labels are drawn on the screen
        self.platforms.draw(self.screen)
        self.screen.fill(White)
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.label,(70,22))
        self.enemy_list.draw(self.screen)
        self.fireballs.draw(self.screen)
        self.enemy_fireballs.draw(self.screen)
        self.hearts.draw(self.screen)
        self.all_sprites.draw(self.screen)
        self.power_ups.draw(self.screen)

        #The display flip is always last in the game loop by drawing the sprite groups
        pygame.display.flip()
        return

    def times_add(self):
        #When level is complete the time and level is saved and appended to the times.txt file
        with open(self.filename,'a') as times: 
            times.write("Your game time - " + str(self.game_minutes) + ":" + str(self.game_seconds) + "  Level - " + str(self.level) + '\n')

    def times_read(self):
        #The backgrounds for the time reading screen are loaded based on the mode of the game
        reading = True
        red_button_background = pygame.transform.rotozoom(pygame.image.load("Red Button Background.jpg"),0,0.8)
        green_button_background = pygame.transform.rotozoom(pygame.image.load("Green_Button_Background.jpg"),0,0.8)
        blue_button_background = pygame.transform.rotozoom(pygame.image.load("Blue_Button_Background.jpg"),0,0.805)
        text_surf = SMALL_TEXT.render("Press Esc to return to main menu.",True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (Width/5, 220)

        #While loop to load when a button is clicked and update the screen's labels and surfaces
        while reading:
            with open(self.filename) as r:
                filecontents = r.read()
            str(filecontents)
            click = False
            self.screen.fill(White)

            #Checks the mode of the game and sets the background
            if self.mode == 'Easy Mode':
                self.screen.blit(red_button_background, (3,0))
            if self.mode == 'Hard Mode':
                self.screen.blit(green_button_background, (3,0))
            if self.mode == 'Master Mode':
                self.screen.blit(blue_button_background, (3,0))
            
            #Uses the ptext module to load the file contents
            ptext.draw(filecontents, (Width/5-117,310), color=White)
            self.screen.blit(text_surf, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_start_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            
            #Checks if the button is pressed and will clear the file contents
            if self.button('C L E A R  T I M E S', Width/5-70,250,BUTTON_WIDTH_SMALL+45,BUTTON_HEIGHT, click, self.inactive_color, self.active_color):
                file = open("times.txt","r+")
                file.truncate(0)
                file.close()
            pygame.display.update()
            self.Clock.tick(FPS)
        return

    def button(self,text, x, y, w, h, click, inactive_colour, active_colour, text_colour=White): #Button function used in all menus for the game
        #Returns the location of the mouse on the screen
        mouse = pygame.mouse.get_pos()
        return_value = False
        
        #If the mouse is on top of the button then the colour is set to active, if clicked then the return value is true
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            pygame.draw.rect(self.screen, active_colour, (x, y, w, h),border_radius=10)
            if click and pygame.time.get_ticks() > 100: 
                return_value = True

        #Else, if mouse not on top of button then set inactive colour
        else:
            pygame.draw.rect(self.screen, inactive_colour, (x, y, w, h),border_radius=10)

        #Set the text in the centre of the button
        text_surf = SMALL_TEXT.render(text,True,text_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        self.screen.blit(text_surf, text_rect)
        return return_value

    def lives_read(self): #Screen for buying lives with coins off the main menu
        reading = True

        #Adds the backgrounds for the menu inluding the text and labels
        red_button_background = pygame.transform.rotozoom(pygame.image.load("Red Button Background.jpg"),0,0.8)
        green_button_background = pygame.transform.rotozoom(pygame.image.load("Green_Button_Background.jpg"),0,0.8)
        blue_button_background = pygame.transform.rotozoom(pygame.image.load("Blue_Button_Background.jpg"),0,0.803)
        text_surf = SMALL_TEXT.render("Press Esc to return to main menu.",True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (Width-(Width/5), 220)
        sprites = pygame.sprite.Group()
        hearts = pygame.sprite.Group()
        coin = Coin(self,Width-(Width/5)-35,250)
        sprites.add(coin)

        #For every health add one heart, for every 3 hearts the hearts move down
        addx = 0
        addy = 0
        for i in range(self.health+self.extra_health):
            hearts.add(Heart(self,Width-(Width/5)+12-addx,380+addy))
            addx += 35
            if addx > 70:
                addy += 30
                addx = 0
            sprites.add(hearts)

        while reading: #While loop to flip menu screen
            self.screen.fill(White)

            #Sets the background and colour of the button based on the mode
            if self.mode == 'Easy Mode':
                self.screen.blit(red_button_background, (0,0))
            if self.mode == "Hard Mode":
                self.screen.blit(green_button_background,(0,0))
            if self.mode == 'Master Mode':
                self.screen.blit(blue_button_background, (0,0))

            #Renders labels
            self.screen.blit(text_surf, text_rect)
            label = self.myfont.render(str(self.coins),True,White)
            click = False

            #Checks if game quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_start_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True

            #Button to buy one life, only can be bought if user has 100 coins or above
            if self.button('B U Y  1  L I F E', Width-(Width/5)-65,300,BUTTON_WIDTH_SMALL+15,BUTTON_HEIGHT, click, self.inactive_color, self.active_color):
                if int(self.coins) >= 100:
                    self.extra_health += 1
                    int(self.coins)
                    self.coins -= 100

                    #Adds another heart to the screen and gives player extra health
                    hearts.add(Heart(self,Width-(Width/5)+12-addx,380+addy))
                    addx += 35
                    if addx > 70:
                        addy += 30
                        addx = 0
                    sprites.add(hearts)
                
            #Draws, updates and flips screen
            sprites.draw(self.screen)
            self.screen.blit(label,(Width-(Width/5)-15,248))
            pygame.display.update()
            pygame.display.flip()
            self.Clock.tick(FPS)
        return

    def left_click_wait(self): #Wait for mouse click function
        waiting = True
        while waiting:
            self.Clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit()

                #When mouse pressed waiting equals false
                if pygame.mouse.get_pressed() == (1,0,0):
                    waiting = False
                    
    def a_or_d_wait(self): #Wait for a, d, left, or right key to be pressed
        waiting = True
        while waiting:
            self.Clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        waiting = False
                    if event.key == pygame.K_d:
                        waiting = False
                    if event.key == pygame.K_LEFT:
                        waiting = False
                    if event.key == pygame.K_RIGHT:
                        waiting = False

    def any_key_wait(self): #Waits for any key to be pressed, clicks dont work
        waiting = True
        while waiting:
            self.Clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    self.playing = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def tutorial_1(self): #When first tutorial is called the text is centred on the tutorial level
        text_surf = HUD_TEXT.render('Welcome to Marlin the Mage! To begin moving the main character use the A or Left key to move left or the D or Right key to move right.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()

        #Waits for keys until game continues
        self.a_or_d_wait()
        self.tutorial_mode_1 = False

        #Sets timer for next tutorial
        pygame.time.set_timer(pygame.USEREVENT + 6, 2000)

    def tutorial_2(self): #Second tutorial teaches user how to kill enemy sprites
        text_surf = HUD_TEXT.render('Now that the game has begun, the enemies, Orc, Wraith and Caster, have started tracking Marlin.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('Try aiming the mouse at an enemy then left click.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+30))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        self.left_click_wait()
        self.tutorial_mode_2 = False
        pygame.time.set_timer(pygame.USEREVENT + 7, 1000)
    
    def tutorial_3(self): #Third tutorial teaches user about all features of the game screen
        text_surf = HUD_TEXT.render('Now you know how to kill the enemies, you must become more aware as to how many lives you have.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('On the top left of the screen are three hearts indicating how many lifes Marlin has before the level is lost.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+30))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('For every enemy killed the coins counter increases by 10 and for every level completed the coins counter increases by 50.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+60))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('The coins can buy more lives from the main menu screen.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+90))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('To continue playing press any key.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+150))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('Use the leaves blocks to hide from the enemy fireballs.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+120))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        self.any_key_wait()
        self.tutorial_mode_3 = False

    def level_selector_screen_setup(self): #Sets the text for the level selector screen, text includes header and mode
        text_surf = MENU_TEXT.render('Levels',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render(self.mode,True,White)
        text_rect = text_surf.get_rect()
        text_rect = (int(Width * 0.01), int(Height * 0.98))
        self.screen.blit(text_surf,text_rect)
        pygame.display.update()
        return

    def level_selector_screen(self): #Level selector screen with wood background
        background = pygame.transform.rotozoom(pygame.image.load("wood_background.png"),0,4.3)
        self.screen.blit(background,(0,0))
        OrcS = Orc(self,Width-(Width/3),Height/3)
        WraithS = Wraith(self,Width-(Width/3),Height-2*(Height/3))
        CasterS = Caster(self,Width-(Width/3),Height-(Height/3))
        sprite = pygame.sprite.Group()
        sprite.add(OrcS)
        sprite.add(WraithS)
        sprite.add(CasterS)
        self.level_selector_screen_setup()
        select = False
        if self.latest_level > 7:
            if self.mode == 'Master Mode':
                self.latest_level = 0
                self.active_color = Menu_Blue
                self.inactive_color = Inactive_Menu_Blue
                self.multiplier = 2
        while select == False: #While loop for level selector menu
            sprite.draw(self.screen)
            click = False

            #Checks if game quit and mouse pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            
            #If hovering over button and mouse clicked then the screen goes to the corresponding game level
            if self.latest_level >= 0:
                if self.button('T U T O R I A L', *button_layout_levels[0], click, self.inactive_color, self.active_color):
                    self.level = 0
                    self.new()
                    select = True
            if self.latest_level >= 4:
                if self.button('L E V E L  4', *button_layout_levels[1], click, self.inactive_color, self.active_color): 
                    self.level = 4
                    self.new()
                    select = True
            else:
                if self.button('L E V E L  4', *button_layout_levels[1], click, Level_Non_Select, Level_Non_Select): 
                    pass
            if self.latest_level >= 1:
                if self.button('L E V E L  1', *button_layout_levels[2], click, self.inactive_color, self.active_color): 
                    self.level = 1
                    self.new()
                    select = True
            else:
                if self.button('L E V E L  1', *button_layout_levels[2], click, Level_Non_Select, Level_Non_Select): 
                    pass
            if self.latest_level >= 5:
                if self.button('L E V E L  5', *button_layout_levels[3], click, self.inactive_color, self.active_color): 
                    self.level = 5
                    self.new()
                    select = True
            else:
                if self.button('L E V E L  5', *button_layout_levels[3], click, Level_Non_Select, Level_Non_Select): 
                    pass
            if self.latest_level >= 2:
                if self.button('L E V E L  2', *button_layout_levels[4], click, self.inactive_color, self.active_color): 
                    self.level = 2
                    self.new()
                    select = True
            else:
                if self.button('L E V E L  2', *button_layout_levels[4], click, Level_Non_Select, Level_Non_Select): 
                    pass
            if self.latest_level >= 6:
                if self.button('L E V E L  6', *button_layout_levels[5], click, self.inactive_color, self.active_color): 
                    self.level = 6
                    self.new()
                    select = True
            else:
                if self.button('L E V E L  6', *button_layout_levels[5], click, Level_Non_Select, Level_Non_Select): 
                    pass
            if self.latest_level >= 3:
                if self.button('L E V E L  3', *button_layout_levels[6], click, self.inactive_color, self.active_color):
                    self.level = 3
                    self.new()
                    select = True
            else:
                if self.button('L E V E L  3', *button_layout_levels[6], click, Level_Non_Select, Level_Non_Select): 
                    pass
            if self.latest_level >= 7:
                if self.button('L E V E L  7', *button_layout_levels[7], click, self.inactive_color, self.active_color): 
                    self.level = 7
                    self.new()
                    select = True
            else:
                if self.button('L E V E L  7', *button_layout_levels[7], click, Level_Non_Select, Level_Non_Select): 
                    pass

            #Buttons to return to main menu and quit game
            if self.button('B A C K', *button_layout_levels[8], click, self.inactive_color, self.active_color): 
                self.show_start_screen()
            if self.button('Q U I T  G A M E', *button_layout_levels[9], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_levels)
            self.Clock.tick(FPS)
        return

    def win_screen_setup(self): #Win menu labels and headers are defined in this function
        self.screen.fill(White)
        if self.level == 0:
            self.win_text = "Tutorial"
            text_surf = MENU_TEXT.render(self.win_text + ' Complete',True,Gold)
        else:
            text_surf = MENU_TEXT.render("Level " + str(self.level) + ' Complete',True,Gold)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        return
    
    def win_screen(self):
        self.win_screen_setup()
        won = True
        while won: #While loop to check if buttons are pressed
            click = False

            #Check for game close and mouse clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True

            #Based on previous level the next level will be played when clicked, only shows when level seven wasn;'t just completed
            if self.latest_level <= 7:
                if self.button('N E X T  L E V E L', *button_layout_5[0],click, self.inactive_color, self.active_color):
                    self.level += 1
                    self.new()
                    won = False

            #Other buttons lead to main menu, times menu and quits game
            if self.button('M A I N  M E N U', *button_layout_5[1], click, self.inactive_color, self.active_color): 
                if self.latest_level >= 7:
                    self.latest_level = 0
                self.show_start_screen()
                won = False
            elif self.button('T I M E S', *button_layout_5[2], click, self.inactive_color, self.active_color): 
                self.times_read()
                won = False
            elif self.button('Q U I T  G A M E', *button_layout_5[3], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_5)
            self.Clock.tick(FPS)
        return

    def settings_screen_setup(self): #Settings screen header label
        self.screen.fill(White)
        text_surf = MENU_TEXT.render('Settings',True,Black)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        return
    
    def settings_screen(self):
        self.settings_screen_setup()
        won = True
        while won: #While loop updates buttons
            #Returns volume of music
            self.volume = pygame.mixer.music.get_volume()

            #If tutorial is active then display true, else false
            if self.tutorial_mode_1 == True:
                tute = 'O N'
            else:
                tute = 'O F F'

            #Returns the value of mode
            if self.mode == 'Easy Mode':
                mode = 'E A S Y'
            elif self.mode == 'Hard Mode':
                mode = 'H A R D'
            elif self.mode == 'Master Mode':
                mode = 'M A S T E R'
            click = False

            #Checks if game quit and mouse clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True

            #If tutoiral button clicked then changes the tutorial mode from true to false or false to true
            if self.button('T U T O R I A L  :  '+tute, *button_layout_settings[0], click, Menu_Settings, Inactive_Menu_Settings):
                if self.tutorial_mode_1 == True:
                    self.tutorial_mode_1 = False
                else:
                    self.tutorial_mode_1 = True

            #Changes the mode to the next level above unless master mode which changes back to easay mode
            elif self.button('M O D E  :  ' + mode, *button_layout_settings[1], click, Menu_Settings, Inactive_Menu_Settings):
                if self.mode == 'Easy Mode':
                    self.mode = 'Hard Mode'
                elif self.mode == 'Hard Mode':
                    self.mode = 'Master Mode'
                elif self.mode == 'Master Mode':
                    self.mode = 'Easy Mode'

            #Displays the value of the volume of music
            elif self.button('V O L U M E  :  ' + str(self.volume), *button_layout_settings[2], click, Menu_Settings, Menu_Settings):
                pass

            #If clicked lowers volume by 0.25 and sound effects
            elif self.button('-', *button_layout_settings[3], click, Menu_Settings, Inactive_Menu_Settings): 
                if self.volume == 0:
                    pass
                else:
                    self.volume -= 0.25
                    pygame.mixer.music.set_volume(self.volume)

            #If clicked increases the volume by 0.25 unless volume is already at 1
            elif self.button('+', *button_layout_settings[4], click, Menu_Settings, Inactive_Menu_Settings): 
                if self.volume == 1:
                    pass
                else:
                    self.volume += 0.25
                    pygame.mixer.music.set_volume(self.volume)

            #Returns to main menu when clicked
            elif self.button('B A C K', *button_layout_settings[5], click, Menu_Settings, Inactive_Menu_Settings): 
                self.show_start_screen()
                won = False
            pygame.display.update(button_layout_settings)
            self.Clock.tick(FPS)
        return

    def game_over_screen_setup(self): #Game over screen labels
        self.screen.fill(Black)
        text_surf = MENU_TEXT.render('Game Over',True,Red)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        return

    def game_over_screen(self):
        self.game_over_screen_setup()
        over = True
        self.enemy_list.empty()
        while over: #While loop updates buttons and labels
            click = False
            #Checks if game quit or mouse clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            
            #If button clicked then game level returns to previous level played
            if self.button('R E S T A R T', *button_layout_4[0], click, self.inactive_color, self.active_color): 
                self.level = self.played_level
                self.new()

            #Returns to main menu, settings or quit game
            elif self.button('M A I N  M E N U', *button_layout_4[1], click, self.inactive_color, self.active_color): 
                self.show_start_screen()
            elif self.button('S E T T I N G S', *button_layout_4[2], click, self.inactive_color, self.active_color):
                self.settings_screen()
                self.game_over_screen_setup()
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_4)
            self.Clock.tick(FPS)
        return

    def show_start_screen_setup(self): #Game main menu screen labels and mode of game
        text_surf = MENU_TEXT.render('Marlin the Mage',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('Created by Luke Nisbett',True,White)
        text_rect = text_surf.get_rect()
        text_rect = (int(Width * 0.83), int(Height * 0.98))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render(self.mode,True,White)
        text_rect = text_surf.get_rect()
        text_rect = (int(Width * 0.01), int(Height * 0.98))
        self.screen.blit(text_surf,text_rect)
        pygame.display.update()
        return

    def show_start_screen(self):
        #Adds the idle player sprite to menu
        Idler = Idle_Menu(Width/2-25,Height-Height/4-40)  

        #Main menu background
        background = pygame.transform.rotozoom(pygame.image.load("wood_background.png"),0,4.3)
        game_begin = False
        self.screen.blit(background,(0,0))
        scores = False
        self.show_start_screen_setup()
        sprite = pygame.sprite.Group()
        sprite.add(Idler)

        #If main menu then music plays for the screen
        if self.menu_music == True:
            pygame.mixer.music.load('Main_Menu_Music.mp3')  
            pygame.mixer.music.play(loops=-1)
            self.menu_music = False
        while scores == False: #While loop updates buttons and screen
            sprite.draw(self.screen)
            click = False
            pressed_keys = pygame.key.get_pressed()
            #Checks if game quit, mouse button pressed, or space bar pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.fadeout(500)
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        game_begin = True
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True

            #Checks the mode of the game and sets the button colours accordingly
            if self.mode == 'Easy Mode':
                self.active_color = Menu_Red
                self.inactive_color = Inactive_Menu_Red
            if self.mode == 'Hard Mode':
                self.active_color = Menu_Green
                self.inactive_color = Inactive_Menu_Green
            if self.mode == 'Master Mode':
                self.active_color = Menu_Blue
                self.inactive_color = Inactive_Menu_Blue

            #Moves the user to level select screen
            if self.button('S T A R T  G A M E', *button_layout_main[0], click, self.inactive_color, self.active_color): 
                game_begin = True

            #Displays the times or lives menu to the main menu
            elif self.button('T I M E S', *button_layout_main[1], click, self.inactive_color, self.active_color): #⏱
                self.times_read()
                scores = True 
            elif self.button('L I V E S', *button_layout_main[2], click, self.inactive_color, self.active_color): #❤
                self.lives_read()

            #Moves to settings menu
            elif self.button('S E T T I N G S', *button_layout_main[3], click, self.inactive_color, self.active_color):
                self.settings_screen()
                self.show_start_screen_setup
            
            #Quits game when pressed
            elif self.button('Q U I T  G A M E', *button_layout_main[4], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            if game_begin:
                while game_begin: 
                    game_begin = self.level_selector_screen()
                    Idler.kill()
                self.show_start_screen_setup
            pygame.display.update(button_layout_main)
            self.Clock.tick(FPS)
            pygame.display.flip()
        return

    def pause_menu_setup(self,background): #Labels for pause menu
        self.screen.blit(background, (0, 0))
        background = self.screen.copy()
        text_surf = MENU_TEXT.render('Paused',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = ((Width // 2), (Height // 4))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        return background


    def pause_menu(self): #Pause menu when escape key pressed during the game running
        paused = True
        #Sets the transparency of the pause menu
        background = pygame.Surface((Width, Height), pygame.SRCALPHA, 32)
        background.fill((*Black, 160))
        background = self.pause_menu_setup(background)
        while paused: #While loop checks buttons and loads menu
            click = False
            pks = pressed_keys = pygame.key.get_pressed()
            #Checks if game quit, a key is pressed or the mouse button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key  == pygame.K_ESCAPE:
                        paused = False
                    elif event.key == pygame.K_m:
                        self.show_start_screen()
                    elif event.key == pygame.K_SPACE: 
                        return
                    elif event.key == pygame.K_q: 
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = True
            
            #If resume then pause menu goes back to game screen
            if self.button('R E S U M E', *button_layout_4[0], click, self.inactive_color, self.active_color): 
                return
            
            #Goes to main menu
            elif self.button('M A I N  M E N U', *button_layout_4[1], click, self.inactive_color, self.active_color): 
                self.player.kill()
                self.enemy_list.empty()
                self.show_start_screen()
                
            #Goes to settings menu
            elif self.button('S E T T I N G S', *button_layout_4[2], click, self.inactive_color, self.active_color):
                self.settings_screen()
                self.pause_menu_setup(background)

            #Quits game
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click, self.inactive_color, self.active_color): 
                sys.exit()
            pygame.display.update(button_layout_4)
            self.Clock.tick(FPS)
        return

#Game function if defined as MtM
MtM = Game()

#Starts game at start screen, main menu
MtM.show_start_screen()