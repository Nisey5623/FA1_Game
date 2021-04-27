import pygame #Maybe add a instructions button to the main menu screen.
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
        self.menu_music = True
        #Variable stating that running is true for game loop below
        self.running = True
        self.shooting = True
        self.enemy_shooting = True
        self.filename = 'times.txt'
        self.enemies = 0
        self.game_delay = True
        self.level = 0
        self.played_level = 0
        self.coins = 0
        self.latest_level = 0
        self.highest_level = 0
        self.mode = 'Easy Mode'
        self.multiplier = 1
        self.background = pygame.image.load("sized_background.jpg")
        self.heart_loss = False
        self.tutorial_mode_1 = True
        self.tutorial_mode_2 = False
        self.tutorial_mode_3 = False
        self.health = 3
        self.extra_health = 0
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
        #Creates a sprite group for all sprites and all platforms
        #Places the player in the scentre of the screen and adds player to all_sprites group
        #self.extra_health = self.health - 3
        pygame.mixer.music.load('Temple Run (iOS) Music- Running Music (128 kbps).mp3') 
        self.menu_music = True
        self.enemies = 0
        self.player = Mage(self,Width/2,668)
        self.health = 3 + self.extra_health
        self.players.add(self.player)
        self.shield = Shield(self,random.randint(100,900),random.randint(100,640))
        self.coin = Coin(self,50,25)
        self.all_sprites.add(self.coin)
        self.power_ups.add(self.shield)
        if self.mode == 'Easy Mode':
            self.active_color = Menu_Red
            self.inactive_color = Inactive_Menu_Red
            self.multiplier = 1
        if self.mode == 'Hard Mode':
            self.tutorial_mode_1 = False
            self.tutorial_mode_2 = False
            self.tutorial_mode_3 = False
            #self.latest_level = 0
            self.active_color = Menu_Green
            self.inactive_color = Inactive_Menu_Green
            self.multiplier = 2
        if self.mode == 'Master Mode':
            self.tutorial_mode_1 = False
            self.tutorial_mode_2 = False
            self.tutorial_mode_3 = False
            #self.latest_level = 0
            self.active_color = Menu_Blue
            self.inactive_color = Inactive_Menu_Blue
            self.multiplier = 3
        add = 0
        for i in range(self.health):
            self.hearts.add(Heart(self,50+add,90))
            add += 35
        self.all_sprites.add(self.hearts)
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
        '''for c in self.caster_list:
            self.platforms.add(platform(c.rect.x, c.rect.y+50,100,20,White))
            self.all_sprites.add(self.platforms)'''
        self.enemy_list.add(self.orc_list)
        self.enemy_list.add(self.caster_list)
        self.enemy_list.add(self.wraith_list)
        self.all_sprites.add(self.player)
        self.wraithupdate = True
        self.hit = False
        #platform_number = random.randint(4,7)
        '''for i in range(0,platform_number):
            p = (platform(random.randint(100,900),random.randint(150,600),random.randint(60,180),20,Black))
            self.all_sprites.add(p)
            self.platforms.add(p)'''
        Platform_non_list = [(0,667,1100,40,Black)] #(947,438),(772,391),(582,358),(274,424),(63,436)
        for plat in Platform_non_list:
            p = platform(*plat)
            #self.all_sprites.add(p)
            self.platforms.add(p)
        Platform_see_list = [(452,400,100,20,Black),(947,438,40,20,Black),(772,391,40,20,Black),(582,358,40,20,Black),(274,424,40,20,Black),(63,436,40,20,Black)]
        for plat in Platform_see_list:
            p = platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.game_seconds = 0
        self.game_minutes = 0 
        self.counts = 0
        #Runs the game loop from below
        self.run()    
        return

    def run(self): #Game Loop
        #Sets the playing variable to while true game updates, checks events and draws while playing is true
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
        self.total_seconds = self.counts // FPS
        self.game_minutes = self.total_seconds // 60
        self.game_seconds = self.total_seconds % 60
        self.counts += 1
        if self.game_minutes > 5:
            self.player.kill()
            self.enemy_list.empty()
            self.game_over_screen()
        self.coins = str(self.coins)
        self.label = self.myfont.render(self.coins,True,White)
        self.all_sprites.update()
        self.enemy_list.update()
        self.enemy_fireballs.update()
        self.fireballs.update()
        self.power_ups.update()
        if self.game_seconds > 0.5:
            for i in self.orc_list:
                self.Orcxdifference = self.player.rect.x - i.rect.x
                if self.Orcxdifference != 0:
                    self.orchspeed = (self.Orcxdifference / self.Orcxdifference * random.randint(1,5))
                    #if self.Orcxdifference > 700:
                        #self.orchspeed = 0
                else:
                    self.orchspeed = 0
                if self.player.rect.x < i.rect.x:
                    i.rect.x -= self.orchspeed
                    i.animate_left()
                if self.player.rect.x > i.rect.x:
                    i.rect.x += self.orchspeed 
                    i.animate_right()
            for w in self.wraith_list:
                Wraithxdifference = self.player.rect.x - w.rect.x
                Wraithydifference = self.player.rect.y - w.rect.y
                if Wraithxdifference != 0:
                    self.wraithhspeed = (Wraithxdifference / Wraithxdifference * random.randint(2,4))
                    #if Wraithxdifference > 700:
                        #self.wraithhspeed = 0
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
            for c in self.caster_list:
                if c.current_frame == 17:
                    if self.enemy_shooting:
                        enemy_fire = Ability(c.rect.x,c.rect.y,self.player.pos.x,self.player.pos.y,14)
                        self.enemy_fireballs.add(enemy_fire)
                        #self.enemy_list.add(self.enemy_fireballs)
                        self.enemy_shooting = False
                        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
                if self.player.rect.x < c.rect.x:
                    c.animate_left()
                if self.player.rect.x > c.rect.x:
                    c.animate_right()
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
        #Check for scrolling
        '''if self.player.rect.right >= (Width - (Width / 4)):
            self.player.pos.x -= max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.x -= max(abs(self.player.vel.x),2)
            for e in self.enemy_list:
                e.rect.x -= max(abs(self.player.vel.x),2)
            for e in self.enemy_fireballs:
                e.rect.centerx -= max(abs(self.player.vel.x),2)
            for s in self.power_ups:
                s.rect.centerx -= max(abs(self.player.vel.x),2)
            for f in self.fireballs:
                f.rect.centerx -= max(abs(self.player.vel.x),2)
        if self.player.rect.left <= Width / 4:
            self.player.pos.x += max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.x += max(abs(self.player.vel.x),2)
            for e in self.enemy_fireballs:
                e.rect.centerx += max(abs(self.player.vel.x),2)
            for e in self.enemy_list:
                e.rect.x += max(abs(self.player.vel.x),2)
            for s in self.power_ups:
                s.rect.x += max(abs(self.player.vel.x),2)
            for f in self.fireballs:
                f.rect.x += max(abs(self.player.vel.x),2)
        return'''
    
    def sprite_collisions(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0):
            #print(mouse_x,mouse_y)
            if self.shooting:
                self.fire = Ability(self.player.pos.x,self.player.pos.y-30, mouse_x, mouse_y,10)
                self.fireballs.add(self.fire)
                self.player.fire_sound.play()
                self.shooting = False
                pygame.time.set_timer(pygame.USEREVENT + 1, 400)
        if pygame.mouse.get_pressed() == (0,1,0):
            if self.platforming:
                self.platformed = platform
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0
                self.player.jumping = False
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
        if self.player.active_shield == False:
            enemyfire_hit = pygame.sprite.spritecollide(self.player,self.enemy_fireballs,False)
            if enemyfire_hit:
                self.health -= 1
        fire_enemy_hit = pygame.sprite.groupcollide(self.enemy_list,self.fireballs, True, True)
        for i in fire_enemy_hit:
            self.enemies -= 1
            self.coins = int(self.coins)
            self.coins += 10
        fire_plat_hit = pygame.sprite.groupcollide(self.fireballs,self.platforms, True, False)
        if self.shield.collect == True:
            shield_activate = pygame.sprite.groupcollide(self.players,self.power_ups,False,False)
            if shield_activate:
                self.shield.rect.x = 45
                self.shield.rect.y = 52
                self.player.active_shield = True
                self.shield.collect = False
                pygame.time.set_timer(pygame.USEREVENT + 4, 5000)
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
            if self.latest_level > 7:
                if self.mode == 'Easy Mode':
                    self.mode = 'Hard Mode'
                else:   
                    self.mode = 'Master Mode'
                #self.latest_level = 0
            self.win_screen()

    def events(self): #Game Loop - Events
        for event in pygame.event.get():
            #Checks if the window is closed to close the game window
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
                pygame.quit()
                sys.exit()
            self.running = False
            if event.type == pygame.USEREVENT + 1:
                self.shooting = True
                pygame.time.set_timer(pygame.USEREVENT + 1,0)
            elif event.type == pygame.USEREVENT + 2:
                self.enemy_shooting = True
                pygame.time.set_timer(pygame.USEREVENT + 2,0)
            elif event.type == pygame.USEREVENT + 3:
                self.hit = False
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)
            elif event.type == pygame.USEREVENT + 4:
                self.player.active_shield = False
                self.shield.collect = True
                self.shield.kill()
                pygame.time.set_timer(pygame.USEREVENT + 4, 0)
            elif event.type == pygame.USEREVENT + 5:
                self.heart_loss = False
                pygame.time.set_timer(pygame.USEREVENT + 5, 0)
            elif event.type == pygame.USEREVENT + 6:
                self.tutorial_mode_2 = True
                pygame.time.set_timer(pygame.USEREVENT + 6, 0)
            elif event.type == pygame.USEREVENT + 7:
                self.tutorial_mode_3 = True
                pygame.time.set_timer(pygame.USEREVENT + 7, 0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.pause_menu()
        return

    def draw(self): #Game Loop - Draw  
        self.platforms.draw(self.screen)
        self.screen.fill(White)
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.label,(70,22))
        
        self.enemy_list.draw(self.screen)
        #self.orc_list.draw(self.screen)
        self.fireballs.draw(self.screen)
        self.enemy_fireballs.draw(self.screen)
        self.hearts.draw(self.screen)
        #pygame.draw.rect(self.screen, Red, self.player.rect)
        #pygame.draw.rect(self.screen, Red, self.enemy.rect)
        self.all_sprites.draw(self.screen)
        self.power_ups.draw(self.screen)
        #The display flip is always last in the game loop.
        pygame.display.flip()
        return

    def times_add(self):
        with open(self.filename,'a') as times: 
            times.write("Your game time - " + str(self.game_minutes) + ":" + str(self.game_seconds) + "  Level - " + str(self.level) + '\n')

    def times_table(self):
        self.scores = pygame.draw.rect(self.screen,Black,((Width/2)-150,(Height - Height)-150,300,300),3)
        self.game_timer = str(self.game_timer)
        scores_surf = SMALL_TEXT.render(self.game_timer,True,Black)
        scores_rect = scores_surf.get_rect()
        scores_rect.center = (int(Width / 2), int(Height - Height))

    def times_read(self):
        reading = True
        red_button_background = pygame.transform.rotozoom(pygame.image.load("Red Button Background.jpg"),0,0.8)
        blue_button_background = pygame.transform.rotozoom(pygame.image.load("Blue_Button_Background.jpg"),0,0.805)
        #self.times_table()        
        text_surf = SMALL_TEXT.render("Press Esc to return to main menu.",True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (Width/5, 220)
        while reading:
            with open(self.filename) as r:
                filecontents = r.read()
            str(filecontents)
            click = False
            self.screen.fill(White)
            if self.mode == 'Easy Mode':
                self.screen.blit(red_button_background, (3,0))
            if self.mode == 'Hard Mode':
                self.screen.blit(red_button_background, (3,0))
            if self.mode == 'Master Mode':
                self.screen.blit(blue_button_background, (3,0))
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
            if self.button('C L E A R  T I M E S', Width/5-70,250,BUTTON_WIDTH_SMALL+45,BUTTON_HEIGHT, click, self.inactive_color, self.active_color):
                file = open("times.txt","r+")
                file.truncate(0)
                file.close()
            pygame.display.update()
            self.Clock.tick(FPS)
        return

    def button(self,text, x, y, w, h, click, inactive_colour, active_colour, text_colour=White):
        mouse = pygame.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            pygame.draw.rect(self.screen, active_colour, (x, y, w, h),border_radius=10)
            if click and pygame.time.get_ticks() > 100: 
                return_value = True
        else:
            pygame.draw.rect(self.screen, inactive_colour, (x, y, w, h),border_radius=10)

        text_surf = SMALL_TEXT.render(text,True,text_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        self.screen.blit(text_surf, text_rect)
        return return_value

    def lives_read(self):
        reading = True
        red_button_background = pygame.transform.rotozoom(pygame.image.load("Red Button Background.jpg"),0,0.8)
        blue_button_background = pygame.transform.rotozoom(pygame.image.load("Blue_Button_Background.jpg"),0,0.803)
        text_surf = SMALL_TEXT.render("Press Esc to return to main menu.",True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (Width-(Width/5), 220)
        sprites = pygame.sprite.Group()
        hearts = pygame.sprite.Group()
        coin = Coin(self,Width-(Width/5)-35,250)
        sprites.add(coin)
        addx = 0
        addy = 0
        for i in range(self.health+self.extra_health):
            hearts.add(Heart(self,Width-(Width/5)+12-addx,380+addy))
            addx += 35
            if addx > 70:
                addy += 30
                addx = 0
            sprites.add(hearts)
        while reading:
            self.screen.fill(White)
            if self.mode == 'Easy Mode':
                self.screen.blit(red_button_background, (0,0))
            if self.mode == 'Master Mode':
                self.screen.blit(blue_button_background, (0,0))
            self.screen.blit(text_surf, text_rect)
            label = self.myfont.render(str(self.coins),True,Black)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.show_start_screen()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            if self.button('B U Y  1  L I F E', Width-(Width/5)-65,300,BUTTON_WIDTH_SMALL+15,BUTTON_HEIGHT, click, self.inactive_color, self.active_color):
                if int(self.coins) >= 100:
                    self.extra_health += 1
                    int(self.coins)
                    self.coins -= 100
                    hearts.add(Heart(self,Width-(Width/5)+12-addx,380+addy))
                    addx += 35
                    if addx > 70:
                        addy += 30
                        addx = 0
                    sprites.add(hearts)
            sprites.draw(self.screen)
            self.screen.blit(label,(Width-(Width/5)-15,248))
            pygame.display.update()
            pygame.display.flip()
            self.Clock.tick(FPS)
        return

    def left_click_wait(self):
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
                if pygame.mouse.get_pressed() == (1,0,0):
                    waiting = False
                    
    def a_or_d_wait(self):
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

    def any_key_wait(self):
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
                if pygame.mouse.get_pressed() == (1,0,0):
                    waiting = False

    def tutorial_1(self):
        text_surf = HUD_TEXT.render('Welcome to Marlin the Mage! To begin moving the main character use the A or Left key to move left or the D or Right key to move right.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        self.a_or_d_wait()
        self.tutorial_mode_1 = False
        pygame.time.set_timer(pygame.USEREVENT + 6, 2000)

    def tutorial_2(self):
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
    
    def tutorial_3(self):
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
        text_surf = HUD_TEXT.render('The coins can buy more lives from the main menu scree.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+90))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('To continue playing press any key.',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 3+120))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        self.any_key_wait()
        self.tutorial_mode_3 = False

    def level_selector_screen_setup(self):
        #self.screen.fill(White)
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

    def level_selector_screen(self):
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
        while select == False:
            sprite.draw(self.screen)
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
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
            if self.button('B A C K', *button_layout_levels[8], click, self.inactive_color, self.active_color): 
                self.show_start_screen()
            if self.button('Q U I T  G A M E', *button_layout_levels[9], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_levels)
            self.Clock.tick(FPS)
        return

    def win_screen_setup(self):
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
        while won:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            if self.latest_level <= 7:
                if self.button('N E X T  L E V E L', *button_layout_5[0],click, self.inactive_color, self.active_color):
                    self.level += 1
                    self.new()
                    won = False
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

    def settings_screen_setup(self):
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
        while won:
            if self.tutorial_mode_1 == True:
                tute = 'O N'
            else:
                tute = 'O F F'
            if self.mode == 'Easy Mode':
                mode = 'E A S Y'
            elif self.mode == 'Hard Mode':
                mode = 'H A R D'
            elif self.mode == 'Master Mode':
                mode = 'M A S T E R'
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            if self.button('T U T O R I A L  :  '+tute, *button_layout_5[0], click, Menu_Settings, Inactive_Menu_Settings):
                if self.tutorial_mode_1 == True:
                    self.tutorial_mode_1 = False
                else:
                    self.tutorial_mode_1 = True
            elif self.button('M O D E  :  ' + mode, *button_layout_5[1], click, Menu_Settings, Inactive_Menu_Settings):
                if self.mode == 'Easy Mode':
                    self.mode = 'Hard Mode'
                elif self.mode == 'Hard Mode':
                    self.mode = 'Master Mode'
                elif self.mode == 'Master Mode':
                    self.mode = 'Easy Mode'
            elif self.button('B A C K', *button_layout_5[2], click, Menu_Settings, Inactive_Menu_Settings): 
                self.show_start_screen()
                won = False
            pygame.display.update(button_layout_5)
            self.Clock.tick(FPS)
        return

    def game_over_screen_setup(self):
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
        while over:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            if self.button('R E S T A R T', *button_layout_4[0], click, self.inactive_color, self.active_color): 
                self.level = self.played_level
                self.new()
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

    def show_start_screen_setup(self): #Game Start Screen
        #self.screen.fill(White)
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
        Idler = Idle_Menu(Width/2-25,Height-Height/4-40)  
        background = pygame.transform.rotozoom(pygame.image.load("wood_background.png"),0,4.3)
        game_begin = False
        self.screen.blit(background,(0,0))
        scores = False
        self.show_start_screen_setup()
        sprite = pygame.sprite.Group()
        sprite.add(Idler)
        if self.menu_music == True:
            pygame.mixer.music.load('Main_Menu_Music.mp3')  
            pygame.mixer.music.play(loops=-1)
            self.menu_music = False
        while scores == False:
            sprite.draw(self.screen)
            click = False
            pressed_keys = pygame.key.get_pressed()
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
            if self.mode == 'Easy Mode':
                self.active_color = Menu_Red
                self.inactive_color = Inactive_Menu_Red
            if self.mode == 'Hard Mode':
                self.active_color = Menu_Green
                self.inactive_color = Inactive_Menu_Green
            if self.mode == 'Master Mode':
                self.active_color = Menu_Blue
                self.inactive_color = Inactive_Menu_Blue
            if self.button('S T A R T  G A M E', *button_layout_main[0], click, self.inactive_color, self.active_color): 
                game_begin = True
            elif self.button('T I M E S', *button_layout_main[1], click, self.inactive_color, self.active_color): #⏱
                self.times_read()
                scores = True 
            elif self.button('L I V E S', *button_layout_main[2], click, self.inactive_color, self.active_color): #❤
                self.lives_read()
            elif self.button('S E T T I N G S', *button_layout_main[3], click, self.inactive_color, self.active_color):
                self.settings_screen()
                self.show_start_screen_setup
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

    def pause_menu_setup(self,background):
        self.screen.blit(background, (0, 0))
        background = self.screen.copy()
        text_surf = MENU_TEXT.render('Paused',True,White)
        text_rect = text_surf.get_rect()
        text_rect.center = ((Width // 2), (Height // 4))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        return background


    def pause_menu(self):
        paused = True
        background = pygame.Surface((Width, Height), pygame.SRCALPHA, 32)
        background.fill((*Black, 160))
        background = self.pause_menu_setup(background)
        while paused:
            click = False
            pks = pressed_keys = pygame.key.get_pressed()
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
            if self.button('R E S U M E', *button_layout_4[0], click, self.inactive_color, self.active_color): 
                return
            elif self.button('M A I N  M E N U', *button_layout_4[1], click, self.inactive_color, self.active_color): 
                self.player.kill()
                self.enemy_list.empty()
                self.show_start_screen()
            elif self.button('S E T T I N G S', *button_layout_4[2], click, self.inactive_color, self.active_color):
                self.settings_screen()
                self.pause_menu_setup(background)
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click, self.inactive_color, self.active_color): 
                sys.exit()
            pygame.display.update(button_layout_4)
            self.Clock.tick(FPS)
        return

MtM = Game()
MtM.show_start_screen()