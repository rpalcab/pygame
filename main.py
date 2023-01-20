import pygame
import sys

pygame.init()       # Starts pygame
screen = pygame.display.set_mode((800,400))     # Creates game window and defines size
pygame.display.set_caption('Runner')            # Names game window

clock = pygame.time.Clock()                     # Creates clock object
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)  # Creates text object

sky_bg = pygame.image.load('graphics/sky.png').convert()          # Import background images. .convert to make it lighter
ground_bg = pygame.image.load('graphics/ground.png').convert()
text_bg = test_font.render('My game', True, 'Black')    # Text to image. Do NOT use convert

# Characters
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # Convert_alpha to respect transparent bg
snail_x_pos = 800                               # Defines initial snail position

player_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 300))          # Creates player rectangle for collisions etc. Topleft indicates reference of rectangle (corner topleft in this case)

while True:                                     # Avoids game from exiting, infinite loop
    for event in pygame.event.get():            # If we want to quit...
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()                          # Cleanly quits
    
    screen.blit(sky_bg, (0,0))                  # Sets background images
    screen.blit(ground_bg, (0,300))
    screen.blit(text_bg, (10,10))
    snail_x_pos -= 4                            # Changes x position with each loop
    if snail_x_pos < -100 : snail_x_pos = 800   # Back to the left
    screen.blit(snail_surface, (snail_x_pos, 265))
    screen.blit(player_surface, player_rect)    # Places player image and rectangle
    pygame.display.update()
    clock.tick(60)                              # Max of 60 times per second, advances in time