import pygame
import sys
import os

#other files for the game
from player import Player
from map_loader import load_map, draw_map, solid, find_spawn, find_checkpoint
from start_menu import StartMenu

#disables cache
sys.dont_write_bytecode = True

#pygame setup
pygame.init()

#fonts
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts", "Micro5-Regular.ttf")
font = pygame.font.Font(FONT_PATH, 46)
checkpoints_font = pygame.font.Font(FONT_PATH, 28)

#screen
screenWidth = 1000
screenHeight = 600

#BG screen
BGcolor = (104, 105, 104)
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Gaming session!")

# background image
try:
    image_path = os.path.join(BASE_DIR, "image",'background.jpg')
    original_image = pygame.image.load(image_path).convert()
    image = pygame.transform.smoothscale(original_image, (screenWidth, screenHeight))
    image_rect = image.get_rect(topleft=(0, 0))
except pygame.error as e:
    print(f"Error loading image: {e}")
    running = False

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

#camera
camera_x = 0
CAMERA_MARGIN = screenWidth * 0.4

#menu
menu = StartMenu(screen, screenWidth, screenHeight)
game_state = "menu"

fade_surface = pygame.Surface((screenWidth, screenHeight))
fade_surface.fill((0, 0, 0))

clock = pygame.time.Clock()
LEVEL_PATH = os.path.join(BASE_DIR, "maps", "level.txt")

def load_level():
    game_map = load_map(LEVEL_PATH)
    solid_tiles, hazard_tiles = solid(game_map)
    SPAWN_X, SPAWN_Y = find_spawn(game_map)
    player = Player(SPAWN_X, SPAWN_Y)
    checkpoints = find_checkpoint(game_map)
    return game_map, player, solid_tiles, hazard_tiles, checkpoints

game_map, player, solid_tiles, hazard_tiles, checkpoints = load_level()

TILE_SIZE = 15
WORLD_HEIGHT = len(game_map) * TILE_SIZE
WORLD_WIDTH = len(game_map[0]) * TILE_SIZE

#checkpoint
current_checkpoint = None
activated_checkpoints = set()
current_checkpoint = player.rect.topleft

checkpoints_message_timer = 0

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            action = menu.handle_event(event)

            if action == "start":
                game_map, player, solid_tiles, hazard_tiles, checkpoints = load_level()
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
        status = player.update(keys, solid_tiles, hazard_tiles, WORLD_WIDTH, WORLD_HEIGHT)

        #check ponint
        for cp in checkpoints[:]:
            if player.rect.colliderect(cp):
                cp_id = (cp.x, cp.y)
            
                if cp_id not in activated_checkpoints:
                    activated_checkpoints.add(cp_id)
                    current_checkpoint = cp.topleft
                    checkpoints.remove(cp)

                    tile_x = cp.x // TILE_SIZE
                    tile_y = cp.y // TILE_SIZE

                    row = list(game_map[tile_y])
                    row[tile_x] = "0"
                    game_map[tile_y] = "".join(row)

                    checkpoints_message_timer = 120

        #camera scrolling
        if player.rect.centerx - camera_x > screenWidth - CAMERA_MARGIN:
            camera_x = player.rect.centerx - (screenWidth - CAMERA_MARGIN)
        elif player.rect.centerx - camera_x < CAMERA_MARGIN:
            camera_x = player.rect.centerx - CAMERA_MARGIN

        camera_x = max(0, min(camera_x, WORLD_WIDTH - screenWidth))

        if status == "dead":
            death_count += 1
            fading = True
            fade_direction = "out"
            show_death_text = True

    #value from the menu
    if game_state == "menu":
        menu.draw()
    elif game_state == "playing":
        screen.fill(BGcolor)
        if 'image' in locals() and image:
            screen.blit(image, (0, 0))
        draw_map(screen, game_map, camera_x)
        player.draw(screen, camera_x)
        player.draw_cooldown(screen, screenWidth)

        death_text = death_font.render(f"Deaths: {death_count}", True, (255, 255, 255))
        screen.blit(death_text, (15, 15))

        #checkpoints
        if checkpoints_message_timer > 0:
            text = checkpoints_text = checkpoints_font.render("Checkpoint reached!", True, (255, 255, 255))
            rect = text.get_rect(center=(screenWidth//2, screenHeight//2))
            screen.blit(text, rect)
            checkpoints_message_timer -= 1

    
    if show_death_text:
        text = font.render("YOU DIED!!!!!!", True, (200, 0, 0))
        text_rect = text.get_rect(center=(screenWidth//2, screenHeight//2))
        screen.blit(text, text_rect)

    #fading screen
    if fading:
        if fade_direction == "out":
            fade_alpha += fade_OUT_speed
            if fade_alpha >= 255:
                fade_alpha = 255

                player = Player(*current_checkpoint)

                #reset the camera to player
                camera_x = player.rect.centerx - screenWidth // 2
                camera_x = max(0, min(camera_x, WORLD_WIDTH - screenWidth))

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