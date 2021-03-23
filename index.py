import pygame
import pygame_menu
import random
import os,sys
from Settings import *
from sprites import *
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
        self.filename = 'times.txt'
        
        

    def new(self): #Start new game
        #Creates a sprite group for all sprites and all platforms
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.fireballs = pygame.sprite.Group()
        self.enemy_fireballs = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.orc_list = pygame.sprite.Group()
        self.caster_list = pygame.sprite.Group()
        pygame.mixer.music.load('Temple Run (iOS) Music- Running Music (128 kbps).mp3')
        #Places the player in the scentre of the screen and adds player to all_sprites group
        self.player = Mage(self)
        enemy_number = random.randint(1,3)
        caster_number = random.randint(0,2)
        for i in range(0,enemy_number):
            self.orc_list.add(Orc(self,random.randint(100,1024),668))
        self.wraith = Wraith(self,300,300)
        for i in range(0,caster_number):
            self.caster_list.add(Caster(self,random.randint(500,2000),random.randint(150,590)))
        for c in self.caster_list:
            self.platforms.add(platform(c.rect.x, c.rect.y+50,100,20,White))
            self.all_sprites.add(self.platforms)
        self.enemy_list.add(self.orc_list)
        self.enemy_list.add(self.caster_list)
        self.enemy_list.add(self.wraith)
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
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.Clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(1000)
        return
    
    def update(self): #Game Loop - Update
        self.game_timer = int(pygame.time.get_ticks()/1000)
        self.all_sprites.update()
        self.enemy_list.update()
        self.orc_list.update()
        self.fireballs.update()
        self.enemy_fireballs.update()
        for i in self.orc_list:
            self.Orcxdifference = self.player.rect.x - i.rect.x
            if self.Orcxdifference != 0:
                self.orchspeed = (self.Orcxdifference / self.Orcxdifference * random.randint(1,5))
                if self.Orcxdifference > 800:
                    self.orchspeed = 0
            else:
                self.orchspeed = 0
            if self.player.rect.x < i.rect.x:
                i.rect.x -= self.orchspeed
                i.animate_left()
            if self.player.rect.x > i.rect.x:
                i.rect.x += self.orchspeed 
                i.animate_right()
        for c in self.caster_list:
            if c.current_frame == 17:
                enemy_fire = Ability(c.rect.x,c.rect.y,self.player.rect.x,self.player.rect.y)
                self.enemy_fireballs.add(enemy_fire)
            if self.player.rect.x < c.rect.x:
                c.animate_left()
            if self.player.rect.x > c.rect.x:
                c.animate_right()
        Wraithxdifference = self.player.rect.x - self.wraith.rect.x
        Wraithydifference = self.player.rect.x - self.wraith.rect.x
        if Wraithxdifference != 0 and Wraithydifference != 0:
            self.wraithhspeed = (Wraithxdifference / Wraithxdifference * 2.5)
            self.wraithvspeed = (Wraithydifference / Wraithydifference * 2.5)
            if Wraithxdifference > 800:
                self.wraithhspeed = 0
        else:
            self.wraithhspeed = 0
            self.wraithvspeed = 0
        if self.player.rect.x < self.wraith.rect.x:
            self.wraith.rect.x -= self.wraithhspeed
            self.wraith.animate_left()
        if self.player.rect.x > self.wraith.rect.x:
            self.wraith.rect.x += self.wraithhspeed 
            self.wraith.animate_right()          
        if self.player.rect.y < self.wraith.rect.y:
            self.wraith.rect.y -= self.wraithvspeed
        if self.player.rect.y > self.wraith.rect.y:
            self.wraith.rect.y += self.wraithvspeed 

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
                if enemy.hit == False:
                    self.player.health -= 1
                    enemy.hit = False
                    self.player.pos.x += 50
                    self.hit = True
                    if self.player.health == 0:
                        self.player.kill()
                        self.game_over_screen()
                    pygame.time.set_timer(pygame.USEREVENT + 3, 2000)
                    timer = 2000 - int(pygame.time.get_ticks()/1000)
                    timer = str(timer)
                    self.hit_timer = self.myfont.render("Time: " + timer,True,(255,255,255))
                    self.screen.blit(self.hit_timer,(self.player.pos.x,self.player.pos.y + 100))
        fire_enemy_hit = pygame.sprite.groupcollide(self.enemy_list,self.fireballs, True, True)
        for i in fire_enemy_hit:
            self.times_add()
            self.win_screen()
        fire_plat_hit = pygame.sprite.groupcollide(self.fireballs,self.platforms, True, False)
        
        
        #Check for scrolling
        if self.player.rect.right >= (Width - (Width / 4)):
            self.player.pos.x -= max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.x -= max(abs(self.player.vel.x),2)
            for e in self.enemy_list:
                e.rect.x -= max(abs(self.player.vel.x),2)
            for e in self.enemy_fireballs:
                e.rect.centerx -= abs(self.player.vel.x)
        if self.player.rect.left <= Width / 4:
            self.player.pos.x += max(abs(self.player.vel.x),2)
            for plat in self.platforms:
                plat.rect.x += max(abs(self.player.vel.x),2)
            for e in self.enemy_fireballs:
                e.rect.centerx += max(abs(self.player.vel.x),2)
            for e in self.enemy_list:
                e.rect.x += max(abs(self.player.vel.x),2)
        return
    
    def events(self): #Game Loop - Events
        for event in pygame.event.get():
            #Checks if the window is closed to close the game window
            if event.type == pygame.QUIT:
                self.playing = False
            self.running = False
            if event.type == pygame.USEREVENT + 1:
                self.shooting = True
                pygame.time.set_timer(pygame.USEREVENT + 1,0)
            if event.type == pygame.USEREVENT + 3:
                self.hit = False
                pygame.time.set_timer(pygame.USEREVENT + 3, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_ESCAPE:
                    self.pause_menu()
        return

    def draw(self): #Game zLoop - Draw  
        background = pygame.image.load("Temple Background.jpg") 
        self.screen.blit(background, (0,0))
        self.enemy_list.draw(self.screen)
        self.orc_list.draw(self.screen)
        self.fireballs.draw(self.screen)
        self.enemy_fireballs.draw(self.screen)
        #pygame.draw.rect(self.screen, Red, self.player.rect)
        #pygame.draw.rect(self.screen, Red, self.enemy.rect)
        self.all_sprites.draw(self.screen)
        #The display flip is always last in the game loop.
        pygame.display.flip()
        return

    def times_add(self):
        with open(self.filename,'a') as times:
            times.write("Your game time : " + str(self.game_timer) + '\n')

    def times_read(self):
        with open(self.filename) as r:
            filecontents = r.read()
        print(filecontents)

    def text_objects(self,text,font,colour=Black):
        text_surface = font.render(text, True, colour)
        return text_surface, text_surface.get_rect()
    
    def button(self,text, x, y, w, h, click, inactive_colour=Blue, active_colour=Light_Blue, text_colour=White):
        mouse = pygame.mouse.get_pos()
        return_value = False
        if x < mouse[0] < x + w and y < mouse[1] < y + h:
            pygame.draw.rect(self.screen, active_colour, (x, y, w, h))
            if click and pygame.time.get_ticks() > 100: 
                return_value = True
        else:
            pygame.draw.rect(self.screen, inactive_colour, (x, y, w, h))

        text_surf, text_rect = self.text_objects(text, SMALL_TEXT, colour=text_colour)
        text_rect.center = (int(x + w / 2), int(y + h / 2))
        self.screen.blit(text_surf, text_rect)
        return return_value

    def win_screen_setup(self):
        self.screen.fill(Black)
        text_surf, text_rect = self.text_objects('Victory',MENU_TEXT, colour=Gold)
        text_rect.center = (int(Width / 2), int(Height / 3))
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
            if self.button('V I E W  T I M E S', *button_layout_4[0], click): 
                self.times_read()
            elif self.button('M A I N  M E N U', *button_layout_4[1], click): 
                self.show_start_screen()
            elif self.button('S E T T I N G S', *button_layout_4[2], click):
                settings_menu()
                self.win_screen_setup()
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_4)
            self.Clock.tick(60)
        return

    def game_over_screen_setup(self):
        self.screen.fill(Black)
        text_surf, text_rect = self.text_objects('Game Over',MENU_TEXT, colour=Red)
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
            if self.button('V I E W  T I M E S', *button_layout_4[0], click): 
                self.times_read()
            elif self.button('M A I N  M E N U', *button_layout_4[1], click): 
                self.show_start_screen()
            elif self.button('S E T T I N G S', *button_layout_4[2], click):
                settings_menu()
                self.game_over_screen_setup()
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click): 
                sys.exit()
                pygame.quit()
            pygame.display.update(button_layout_4)
            pygame.display.update(button_layout_4)
            self.Clock.tick(60)
        return

    def show_start_screen_setup(self): #Game Start Screen
        self.screen.fill(White)
        text_surf, text_rect = self.text_objects('Marlin the Mage',MENU_TEXT)
        text_rect.center = (int(Width / 2), int(Height / 4))
        self.screen.blit(text_surf, text_rect)
        text_surf, text_rect = self.text_objects(f'v{1.0}', SMALL_TEXT)
        text_rect.center = (int(Width - Width * 0.98), int(Height - Height * 0.98))
        self.screen.blit(text_surf, text_rect)
        text_surf, text_rect = self.text_objects('Created by Luke Nisbett', LARGE_TEXT)
        text_rect.center = (int(Width / 2), int(Height * 0.84))
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        return

    def show_start_screen(self):
        self.show_start_screen_setup()
        game_begin = view_hs = False
        while True:
            click = False
            pressed_keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_SPACE:
                        self.new
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_v or event.key == pygame.K_h): 
                    view_hs = True
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    click = True
            if self.button('S T A R T  G A M E', *button_layout_4[0], click): 
                game_begin = True
            elif self.button('V I E W  T I M E S', *button_layout_4[1], click) or view_hs:
                self.times_read()
            elif self.button('S E T T I N G S', *button_layout_4[2], click):
                settings_menu()
                self.show_start_screen_setup
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click): 
                sys.exit()
                pygame.quit()
            if game_begin:
                while game_begin: 
                    game_begin = self.new() == 'Restart'
                self.show_start_screen_setup
            pygame.display.update(button_layout_4)
            self.Clock.tick(60)
        return

    def pause_menu_setup(self,background):
        self.screen.blit(background, (0, 0))
        background = self.screen.copy()
        text_surf, text_rect = self.text_objects('Paused', MENU_TEXT, colour=White)
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
            if self.button('R E S U M E', *button_layout_4[0], click): 
                return
            if self.button('M A I N  M E N U', *button_layout_4[1], click): 
                self.show_start_screen()
            if self.button('S E T T I N G S', *button_layout_4[2], click):
                settings_menu()
                self.pause_menu_setup(background)
            elif self.button('Q U I T  G A M E', *button_layout_4[3], click): sys.exit()
            pygame.display.update(button_layout_4)
            self.Clock.tick(60)
        return

MtM = Game()
MtM.show_start_screen()