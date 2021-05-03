import pygame
#Initializes pygame.font for buttons and text sizes
pygame.font.init()
#Sets the width and the height for the game display.
Width = 1024
Height = 768
#Sets game speed.
FPS = 60
#Defined variables such as colour for buttons and text
White = (255,255,255)
Black = (0,0,0)
Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
ALPHA = (0,255,0)
Light_Blue = (0,191,255)
Gold = (139,117,0)
Level_Non_Select = (77, 77, 77)
Menu_Red = (127,0,0)
Inactive_Menu_Red = (189,30,2)
Menu_Green = (0, 204, 102)
Inactive_Menu_Green = (0, 153, 77)
Menu_Blue = (0,0,127)
Inactive_Menu_Blue = (2,30,209)
Menu_Settings = (102,102,102)
Inactive_Menu_Settings = (179,179,179)

#Fonts of bold, regular and light of calibri
FONT_BOLD = pygame.font.match_font('Calibri-SemiBold')
FONT_REG = pygame.font.match_font('Calibri-Regular')
FONT_LIGHT = pygame.font.match_font('Calibri-Light')

#Sizes for each text based on font and text width by height
MENU_TEXT = pygame.font.Font(FONT_LIGHT, int(110 / 1080 * Height))
LARGE_TEXT = pygame.font.Font(FONT_REG, int(60 / 1080 * Height))
MEDIUM_TEXT = pygame.font.Font(FONT_LIGHT, int(50 / 1440 * Height))
SMALL_TEXT = pygame.font.Font(FONT_BOLD, int(45 / 1440 * Height))
HUD_TEXT = pygame.font.Font(FONT_REG, int(40 / 1440 * Height))

#All widths and heights are defined for menus
BUTTON_WIDTH = int(Width * 0.625 // 3)
BUTTON_WIDTH_SMALL = int(Width * 0.625 // 3 / 2)
BUTTON_WIDTH_VERY_SMALL = int(Width * 0.625 // 3 / 4)
BUTTON_HEIGHT = int(Height * 5 // 81)
button_x_start = (Width - BUTTON_WIDTH) // 2
LEVEL_QUIT_BUTTON = int(Width * 0.625 // 3) +20

#Layouts for the button function in the index file
button_layout_4 = [(button_x_start, Height * 5 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 6 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 7 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 8 // 13, BUTTON_WIDTH, BUTTON_HEIGHT)]
button_layout_main = [(button_x_start, Height * 5 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 6 // 13, BUTTON_WIDTH_SMALL-10, BUTTON_HEIGHT),
                       (button_x_start+BUTTON_WIDTH_SMALL+10, Height * 6 // 13, BUTTON_WIDTH_SMALL-10, BUTTON_HEIGHT),
                       (button_x_start, Height * 7 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 8 // 13, BUTTON_WIDTH, BUTTON_HEIGHT)]
button_layout_levels = [(button_x_start-10, Height * 4 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start+BUTTON_WIDTH_SMALL+10, Height * 4 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start-10, Height * 5 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start+BUTTON_WIDTH_SMALL+10, Height * 5 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start-10, Height * 6 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start+BUTTON_WIDTH_SMALL+10, Height * 6 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start-10, Height * 7 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start+BUTTON_WIDTH_SMALL+10, Height * 7 // 13, BUTTON_WIDTH_SMALL, BUTTON_HEIGHT),
                       (button_x_start-10, Height * 8 // 13, LEVEL_QUIT_BUTTON, BUTTON_HEIGHT),
                       (button_x_start-10, Height * 9 // 13, LEVEL_QUIT_BUTTON, BUTTON_HEIGHT)]
button_layout_5 = [(button_x_start, Height * 5 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 6 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 7 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 8 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 9 // 13, BUTTON_WIDTH, BUTTON_HEIGHT)]
button_layout_settings = [(button_x_start, Height * 5 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 6 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start, Height * 7 // 13, BUTTON_WIDTH, BUTTON_HEIGHT),
                       (button_x_start+BUTTON_WIDTH_VERY_SMALL-125, Height * 7 // 13, BUTTON_WIDTH_VERY_SMALL, BUTTON_HEIGHT),
                       (button_x_start+BUTTON_WIDTH+19, Height * 7 // 13, BUTTON_WIDTH_VERY_SMALL, BUTTON_HEIGHT),
                       (button_x_start, Height * 8 // 13, BUTTON_WIDTH, BUTTON_HEIGHT)]

#Defined the player acceleration and player friction for the mage function
PLAYER_ACC = 1
PLAYER_FRICTION = -0.12