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
        #Variable stating that running is true for game loop below
        self.running = True
        self.shooting = True
        self.enemy_shooting = True
        self.filename = 'times.txt'
        self.enemies = 0
        self.game_delay = True
        self.level = 0
        self.coins = 0
        self.latest_level = 0
        self.mode = 'Easy Mode'
        self.multiplier = 1
        

    def new(self): #Start new game
        #Creates a sprite group for all sprites and all platforms
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
        pygame.mixer.music.load('Temple Run (iOS) Music- Running Music (128 kbps).mp3')
        #Places the player in the scentre of the screen and adds player to all_sprites group
        self.player = Mage(self,Width/2,Height/2)
        self.player.health = 3
        self.players.add(self.player)
        self.shield = Shield(self,300,100)
        self.coin = Coin(self,50,25)
        self.all_sprites.add(self.coin)
        self.power_ups.add(self.shield)
        add = 0
        for i in range(self.player.health):
            self.heart = Heart(self,50+add,75)
            self.hearts.add(self.heart)
            add += 35
        if self.level == 0:
            enemy_number = 1 * self.multiplier
            wraith_number = 1 * self.multiplier
            caster_number = 1 * self.multiplier
        if self.level == 1:
            enemy_number = random.randint(1,2) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = 1 * self.multiplier
        if self.level == 2:
            enemy_number = random.randint(1,3) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
        if self.level == 3:
            enemy_number = random.randint(1,2) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = 1 * self.multiplier
        if self.level == 4:
            enemy_number = random.randint(1,3) * self.multiplier
            wraith_number = random.randint(1,2) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
        if self.level == 5:
            enemy_number = random.randint(2,3) * self.multiplier
            wraith_number = random.randint(1,3) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
        if self.level == 6:
            enemy_number = random.randint(2,3) * self.multiplier
            wraith_number = random.randint(2,3) * self.multiplier
            caster_number = random.randint(1,2) * self.multiplier
        if self.level == 7:
            enemy_number = random.randint(3,4) * self.multiplier
            wraith_number = 3 * self.multiplier
            caster_number = 3 * self.multiplier
        for i in range(0,enemy_number):
            self.orc_list.add(Orc(self,random.randint(100,1024),668))
            self.enemies += 1
        for i in range(0,wraith_number):
            self.wraith_list.add(Wraith(self,random.randint(100,1800),random.randint(200,400)))
            self.enemies += 1
        for i in range(0,caster_number):
            self.caster_list.add(Caster(self,random.randint(500,1800),random.randint(150,400)))
            self.enemies += 1
        for c in self.caster_list:
            self.platforms.add(platform(c.rect.x, c.rect.y+50,100,20,White))
            self.all_sprites.add(self.platforms)
        self.enemy_list.add(self.orc_list)
        self.enemy_list.add(self.caster_list)
        self.enemy_list.add(self.wraith_list)
        self.all_sprites.add(self.player)
        self.wraithupdate = True
        self.hit = False
        platform_number = random.randint(6,12)
        for i in range(0,platform_number):
            p = (platform(random.randint(100,1800),random.randint(150,600),random.randint(60,180),20,Black))
            self.all_sprites.add(p)
            self.platforms.add(p)
        Platform_list = [(0,Height - 40,2000,40,Black),(Width / 2-50,520,100,20,Black),(0,0,40,800,Black)]
        for plat in Platform_list:
            p = platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)
        self.game_seconds = 0
        self.game_minutes = 0 
        self.counts = 0
        if self.mode == 'Easy Mode':
            self.active_color = Menu_Red
            self.inactive_color = Inactive_Menu_Red
            self.multiplier = 1
        if self.mode == 'Master Mode':
            self.active_color = Menu_Blue
            self.inactive_color = Inactive_Menu_Blue
            self.multiplier = 2
        #Runs the game loop from below
        self.run()    
        return

    def run(self): #Game Loop
        #Sets the playing variable to while true game updates, checks events and draws while playing is true
        #pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.Clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        #pygame.mixer.music.fadeout(1000)
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
        self.label = self.myfont.render(self.coins,True,Black)
        self.all_sprites.update()
        self.enemy_list.update()
        self.orc_list.update()
        self.fireballs.update()
        self.enemy_fireballs.update()
        self.power_ups.update()
        if self.game_seconds > 1:
            for i in self.orc_list:
                self.Orcxdifference = self.player.rect.x - i.rect.x
                if self.Orcxdifference != 0:
                    self.orchspeed = (self.Orcxdifference / self.Orcxdifference * random.randint(1,5))
                    if self.Orcxdifference > 700:
                        self.orchspeed = 0
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
                    if Wraithxdifference > 700:
                        self.wraithhspeed = 0
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
                        self.enemy_shooting = False
                        pygame.time.set_timer(pygame.USEREVENT + 2, 1000)
                if self.player.rect.x < c.rect.x:
                    c.animate_left()
                if self.player.rect.x > c.rect.x:
                    c.animate_right()
        self.sprite_collisions()
        #Check for scrolling
        if self.player.rect.right >= (Width - (Width / 4)):
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
        return
    
    def sprite_collisions(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1,0,0):
            if self.shooting:
                self.fire = Ability(self.player.pos.x,self.player.pos.y-30, mouse_x, mouse_y,7)
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
            if self.player.active_shield == False:
                hit_list = pygame.sprite.spritecollide(self.player, self.enemy_list, False)
                for enemy in hit_list:
                    if enemy.hit == False:
                        self.player.health -= 1
                        self.hearts.remove()
                        self.hearts.update()
                        enemy.hit = False
                        self.player.pos.x += 50
                        self.hit = True
                        self.timer = pygame.time.set_timer(pygame.USEREVENT + 3, 2000)
                        if self.player.health == 0:
                            self.player.kill()
                            self.enemy_list.empty()
                            self.game_over_screen()
                        
        if self.hit == True:
            self.timer = str(self.timer)
            self.hit_timer = self.myfont.render("Time: " + self.timer,True,Black)

                    
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
        if self.enemies == 0:
            self.times_add()
            self.player.kill()
            self.enemy_list.empty()
            self.latest_level += 1
            self.coins += 50
            if self.latest_level > 7:
                self.mode = 'Master Mode'
            self.win_screen()

    def events(self): #Game Loop - Events
        for event in pygame.event.get():
            #Checks if the window is closed to close the game window
            if event.type == pygame.QUIT:
                self.playing = False
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.pause_menu()
        return

    def draw(self): #Game zLoop - Draw  
        background = pygame.image.load("Temple Background.jpg") 
        #self.screen.blit(background, (0,0))
        self.screen.fill(White)
        self.screen.blit(self.label,(70,22))
        self.power_ups.draw(self.screen)
        self.enemy_list.draw(self.screen)
        self.orc_list.draw(self.screen)
        self.fireballs.draw(self.screen)
        self.enemy_fireballs.draw(self.screen)
        self.hearts.draw(self.screen)
        if self.hit == True:
            self.screen.blit(self.hit_timer,(self.player.pos.x,self.player.pos.y - 100))
        #pygame.draw.rect(self.screen, Red, self.player.rect)
        #pygame.draw.rect(self.screen, Red, self.enemy.rect)
        self.all_sprites.draw(self.screen)
        #The display flip is always last in the game loop.
        pygame.display.flip()
        return

    def times_add(self):
        with open(self.filename,'a') as times: 
            times.write("Your game time - " + str(self.game_minutes) + ":" + str(self.game_seconds) + '\n')

    def times_table(self):
        self.scores = pygame.draw.rect(self.screen,Black,((Width/2)-150,(Height/2)-150,300,300),3)
        self.game_timer = str(self.game_timer)
        scores_surf = SMALL_TEXT.render(self.game_timer,True,Black)
        scores_rect = scores_surf.get_rect()
        scores_rect.center = (int(Width / 2), int(Height / 3))

    def times_read(self):
        reading = True
        with open(self.filename) as r:
            filecontents = r.read()
        str(filecontents) #Luke for times add a box with 10 of the lowest times that the game has been completed. Also change the goal of the game to unlock a door when all enemies are dead
        self.screen.fill(White)
        #self.times_table()        
        '''text_surf = MEDIUM_TEXT.render(filecontents,True,Black)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)'''
        ptext.draw(filecontents, (400,400), color=Blue)
        while reading:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
            pygame.display.update()
            self.Clock.tick(FPS)
        return

    def button(self,text, x, y, w, h, click, inactive_colour, active_colour, text_colour=White):
        mouse = pygame.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            pygame.draw.rect(self.screen, active_colour, (x, y, w, h))
            if click and pygame.time.get_ticks() > 100: 
                return_value = True
        else:
            pygame.draw.rect(self.screen, inactive_colour, (x, y, w, h))

        text_surf = SMALL_TEXT.render(text,True,text_colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        self.screen.blit(text_surf, text_rect)
        return return_value

    def level_selector_screen_setup(self):
        self.screen.fill(White)
        text_surf = MENU_TEXT.render('Levels',True,Black)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render(self.mode,True,Black)
        text_rect = text_surf.get_rect()
        text_rect = (int(Width * 0.01), int(Height * 0.98))
        self.screen.blit(text_surf,text_rect)
        pygame.display.update()
        return

    def level_selector_screen(self):
        self.level_selector_screen_setup()
        select = False
        while select == False:
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
            if self.latest_level >= 1:
                if self.button('L E V E L  1', *button_layout_levels[2], click, self.inactive_color, self.active_color): 
                    self.level = 1
                    self.new()
                    select = True
            if self.latest_level >= 5:
                if self.button('L E V E L  5', *button_layout_levels[3], click, self.inactive_color, self.active_color): 
                    self.level = 5
                    self.new()
                    select = True
            if self.latest_level >= 2:
                if self.button('L E V E L  2', *button_layout_levels[4], click, self.inactive_color, self.active_color): 
                    self.level = 2
                    self.new()
                    select = True
            if self.latest_level >= 6:
                if self.button('L E V E L  6', *button_layout_levels[5], click, self.inactive_color, self.active_color): 
                    self.level = 6
                    self.new()
                    select = True
            if self.latest_level >= 3:
                if self.button('L E V E L  3', *button_layout_levels[6], click, self.inactive_color, self.active_color):
                    self.level = 3
                    self.new()
                    select = True
            if self.latest_level >= 7:
                if self.button('L E V E L  7', *button_layout_levels[7], click, self.inactive_color, self.active_color): 
                    self.level = 7
                    self.new()
                    select = True
            if self.button('M A I N  M E N U', *button_layout_levels[8], click, self.inactive_color, self.active_color): 
                self.show_start_screen()
            if self.button('Q U I T  G A M E', *button_layout_levels[9], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_levels)
            self.Clock.tick(60)
        return

    def win_screen_setup(self):
        self.screen.fill(White)
        text_surf = MENU_TEXT.render('Level Complete',True,Gold)
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
            if self.button('L E V E L S', *button_layout_5[0],click, self.inactive_color, self.active_color):
                self.level_selector_screen()
                won = False
            elif self.button('T I M E S', *button_layout_5[1], click, self.inactive_color, self.active_color): 
                self.times_read()
                won = False
            elif self.button('M A I N  M E N U', *button_layout_5[2], click, self.inactive_color, self.active_color): 
                self.show_start_screen()
                won = False
            elif self.button('S E T T I N G S', *button_layout_5[3], click, self.inactive_color, self.active_color):
                settings_menu()
                self.win_screen_setup()
            elif self.button('Q U I T  G A M E', *button_layout_5[4], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_5)
            self.Clock.tick(60)
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
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            if self.button('M A I N  M E N U', *button_layout_5[2], click, Menu_Settings, Inactive_Menu_Settings): 
                self.show_start_screen()
                won = False
            pygame.display.update(button_layout_5)
            self.Clock.tick(60)
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
        while over:
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            if self.button('T I M E S', *button_layout_4[0], click, self.inactive_color, self.active_color): 
                self.times_read()
            elif self.button('M A I N  M E N U', *button_layout_4[1], click, self.inactive_color, self.active_color): 
                self.show_start_screen()
            elif self.button('S E T T I N G S', *button_layout_4[2], click, self.inactive_color, self.active_color):
                self.settings_screen()
                self.game_over_screen_setup()
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click, self.inactive_color, self.active_color): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_4)
            self.Clock.tick(60)
        return

    def show_start_screen_setup(self): #Game Start Screen
        self.screen.fill(White)
        text_surf = MENU_TEXT.render('Marlin the Mage',True,Black)
        text_rect = text_surf.get_rect()
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render('Created by Luke Nisbett',True,Black)
        text_rect = text_surf.get_rect()
        text_rect = (int(Width * 0.83), int(Height * 0.98))
        self.screen.blit(text_surf, text_rect)
        text_surf = HUD_TEXT.render(self.mode,True,Black)
        text_rect = text_surf.get_rect()
        text_rect = (int(Width * 0.01), int(Height * 0.98))
        self.screen.blit(text_surf,text_rect)
        pygame.display.update()
        return

    def show_start_screen(self):
        Idler = Idle_Menu(Width/2-25,Height-Height/4-40)
        self.show_start_screen_setup()
        game_begin = False
        scores = False
        while scores == False:
            sprite = pygame.sprite.Group()
            sprite.add(Idler)
            sprite.draw(self.screen)
            click = False
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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
            if self.mode == 'Master Mode':
                self.active_color = Menu_Blue
                self.inactive_color = Inactive_Menu_Blue
            if self.button('S T A R T  G A M E', *button_layout_main[0], click, self.inactive_color, self.active_color): 
                game_begin = True
            elif self.button('T I M E S', *button_layout_main[1], click, self.inactive_color, self.active_color): #⏱
                self.times_read()
                scores = True 
            elif self.button('L I V E S', *button_layout_main[2], click, self.inactive_color, self.active_color): #❤
                print(self.player.health)
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
            self.Clock.tick(60)
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
                self.show_start_screen()
            elif self.button('S E T T I N G S', *button_layout_4[2], click, self.inactive_color, self.active_color):
                self.settings_screen()
                self.pause_menu_setup(background)
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click, self.inactive_color, self.active_color): 
                sys.exit()
            pygame.display.update(button_layout_4)
            self.Clock.tick(60)
        return

MtM = Game()
MtM.show_start_screen()