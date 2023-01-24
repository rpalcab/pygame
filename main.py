import pygame
from sys import exit
from time import sleep

## Functions
def display_score():
    current_time = pygame.time.get_ticks() // 500 - start_time
    score_surf = font_score.render(f'Score: {current_time}', False, (64,64,64))    # Text to image, color in HEX format. Do NOT use convert
    score_rect = score_surf.get_rect(midtop = (400, 20))
    screen.blit(score_surf, score_rect)
    return current_time

def set_bg():
    screen.blit(sky_bg, (0,0))                  # Sets background images
    screen.blit(ground_bg, (0,300))
    return None

def snail_mv(current_time):
    ini_speed = 6
    extra_speed = (current_time // 20)          # Snail speed increases with time
    snail_rect.x -= ini_speed + extra_speed             # Moves snail to the left
    if snail_rect.right <= 0: snail_rect.left = 800     # Snail goes back to the right
    screen.blit(snail_surf, snail_rect)      # Places snail
    return None

def player_mv(player_gravity):
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 300: player_rect.bottom = 300
    screen.blit(player_surf, player_rect)    # Places player image and rectangle
    return player_rect, player_gravity

def end_screen(current_time, score_surf, score_rect):
    current_time = pygame.time.get_ticks() // 1000 - start_time
    screen.fill('Black')
    screen.blit(title_surf, title_rect) 
    screen.blit(player_stand, player_stand_rect)
    screen.blit(score_surf, score_rect)   
    if current_time%2 == 1:
        screen.blit(space_surf, space_rect)
    return current_time

## Initial setup
pygame.init()       # Starts pygame
screen = pygame.display.set_mode((800,400))     # Creates game window and defines size
pygame.display.set_caption('Runner')            # Names game window
FPS=60
game_active  = False
start_time = 0

## Clock
clock = pygame.time.Clock()                     # Creates clock object
current_time = pygame.time.get_ticks() // 500 - start_time

## Fonts
font_title = pygame.font.Font('font/Pixeltype.ttf', 75)
font_score = pygame.font.Font('font/Pixeltype.ttf', 50)  # Creates text object

## Score
highest_score = 0
score_surf = font_score.render(f'Highest score: {highest_score}', False, 'White')
score_rect = score_surf.get_rect(midleft = (25, 40))

## Images
# Game background
sky_bg = pygame.image.load('graphics/sky.png').convert()          # Import background images. .convert to make it lighter
ground_bg = pygame.image.load('graphics/ground.png').convert()

# Start/end background
title_surf = font_title.render(f'Runner', False, 'White')    # Text to image, color in HEX format. Do NOT use convert
title_rect = title_surf.get_rect(midtop = (400, 20))

space_surf = font_score.render(f'Press space to start', False, 'White')
space_rect = space_surf.get_rect(midtop = (400, 325))

# Characters
snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # Convert_alpha to respect transparent bg
snail_rect = snail_surf.get_rect(bottomleft = (800, 300))

player_surf = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))          # Creates player rectangle for collisions etc. Topleft indicates reference of rectangle (corner topleft in this case)
player_gravity = 0

player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
# player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = ((400,200))) 

# Game starts
while True:                                     # Avoids game from exiting, infinite loop
    # Event check
    for event in pygame.event.get():
        # Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()                          # Cleanly quits

        if game_active:
            # Move horizontally with "a" and "d"
            keys = pygame.key.get_pressed()
            if keys[ord('a')]:
                player_rect.x -= 4
            if keys[ord('d')]:
                player_rect.x += 4
            # Move vertically
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Jump if left click
                if pygame.mouse.get_pressed() == (1, 0, 0) and player_rect.bottom == 300:
                    player_gravity = -20
                # Down in right click
                if pygame.mouse.get_pressed() == (0, 0, 1):
                    player_gravity = 25

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.left = 800
                player_rect.midbottom = (80, 300)
                start_time = pygame.time.get_ticks() // 500


    if game_active:
        # Sets background
        set_bg()
        
        # Sets score
        current_time = display_score()

        # Snail position and movement
        snail_mv(current_time)

        # Player position and movement
        player_rect, player_gravity = player_mv(player_gravity)

        # Player/Snail collision
        if player_rect.colliderect(snail_rect):        # Check if player collides with snail
            ## IDEA: Make player blink and then black screen
            game_active = False
            if current_time > highest_score:
                highest_score = current_time
                score_surf = font_score.render(f'Highest score: {highest_score}', False, 'White')
                score_rect = score_surf.get_rect(midleft = (25, 40))
            ## IDEA: Make gradient black screen
    else:
        current_time = end_screen(current_time, score_surf, score_rect)
    
    # Time passes
    pygame.display.update()
    clock.tick(FPS)                              # Max of 60 times per second, advances in time


# Cool thing I'm probably gonna use in the future:
    # Inside event loop
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if player_rect.collidepoint(event.pos):
        #         player_gravity = -20
        # # IDEA: Crush snails if you press them (any mouse button)   # Checks mouse position and if it collides with characters
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print('OUCH')
        #         print(pygame.mouse.get_pressed())
        #     if snail_rect.collidepoint(event.pos):
        #         print('PRFT...')
        #         print(pygame.mouse.get_pressed())


        # Line moving with mouse
        # pygame.draw.line(screen, 'Black', (0,0), pygame.mouse.get_pos(), 10)      # Draws a line from the topleft to the mouse