import pygame
import sys
import os

#other files for the game
from player import Player
from map_loader import load_map, draw_map, solid
from start_menu import StartMenu

#disables cache
sys.dont_write_bytecode = True

#pygame setup
pygame.init()

#fonts
BASE_DIR = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_DIR, "fonts", "Micro5-Regular.ttf")
font = pygame.font.Font(FONT_PATH, 46)

#screen
screenWidth = 1000
screenHeight = 600
BGcolor = (104, 105, 104)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Gaming session!")

#fade screen
fade_alpha = 0
fade_OUT_speed = 4
fade_IN_speed = 15
fading = False
fade_direction = "out"
show_death_text = False

#death count
death_count = 0
death_font = pygame.font.Font(FONT_PATH, 18)

#menu
menu = StartMenu(screen, screenWidth, screenHeight)
game_state = "menu"

fade_surface = pygame.Surface((screenWidth, screenHeight))
fade_surface.fill((0, 0, 0))

clock = pygame.time.Clock()
BASE_DIR = os.path.dirname(__file__)
LEVEL_PATH = os.path.join(BASE_DIR, "maps", "level1.txt")

def load_level():
    game_map = load_map(LEVEL_PATH)
    solid_tiles = solid(game_map)
    player = Player(50, 50)
    return game_map, player, solid_tiles

game_map, player, solid_tiles = load_level()

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            action = menu.handle_event(event)

            if action == "start":
                game_map, player, solid_tiles = load_level()
                death_count = 0
                fade_alpha = 0
                game_state = "playing"
            elif action == "quit":
                running = False
        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                    player.jump()

    #get the keys
    keys = pygame.key.get_pressed()

    if not fading:
        status = player.update(keys, solid_tiles, screenWidth, screenHeight)

        if status == "dead":
            death_count += 1
            fading = True
            fade_direction = "out"
            show_death_text = True

    if game_state == "menu":
        menu.draw()
    elif game_state == "playing":
        screen.fill(BGcolor)
        draw_map(screen, game_map)
        player.draw(screen)
        player.draw_cooldown(screen, screenWidth)

        death_text = death_font.render(f"Deaths: {death_count}", True, (0, 0, 0))
        screen.blit(death_text, (15, 15))

    
    if show_death_text:
        text = font.render("YOU DIED!!!!!!", True, (200, 0, 0))
        text_rect = text.get_rect(center=(screenWidth//2, screenHeight//2))
        screen.blit(text, text_rect)

    if fading:
        if fade_direction == "out":
            fade_alpha += fade_OUT_speed
            if fade_alpha >= 255:
                fade_alpha = 255

                game_map, player, solid_tiles = load_level()
                fade_direction = "in"
                show_death_text = False
        elif fade_direction == "in":
            fade_alpha -= fade_IN_speed
            if fade_alpha <= 0:
                fade_alpha = 0
                fading = False
    
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
    
    pygame.display.flip()

    clock.tick(60) #set the fps 60

pygame.quit()
sys.exit()
