import pygame
import math
import os

pygame.init()

TILE_SIZE = 15

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "..", "image")
STONE_PATH = os.path.join(IMAGE_DIR, "stone.png")

# background image
try:
    stone_tile = pygame.image.load(STONE_PATH).convert_alpha()
    stone_tile = pygame.transform.smoothscale(stone_tile, (TILE_SIZE, TILE_SIZE))
except Exception as e:
    raise SystemExit("ERROR")

def load_map(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]
    
def find_spawn(game_map):
    for y, row in enumerate(game_map):
        for x, col in enumerate(row):
            if col == "S":
                return x * TILE_SIZE, y * TILE_SIZE
    return 50, 50

def find_checkpoint(game_map):
    checkpoints = []
    for y, row in enumerate(game_map):
        for x, col in enumerate(row):
            if col == "C":
                rect = pygame.Rect(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
                checkpoints.append(rect)
    return checkpoints
    
def solid(game_map):
    solid_tiles = []
    hazard_tiles = []

    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            
            if tile == "1":
                solid_tiles.append(rect)
            elif tile in ("~", "^"):
                hazard_tiles.append(rect)
    return solid_tiles, hazard_tiles

def draw_map(surface, game_map, camera_x):
    for y, row in enumerate(game_map):
        for x, tile in enumerate(row):
            screen_rect = pygame.Rect(
                x * TILE_SIZE - camera_x,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )

            if tile == "1":
                surface.blit(stone_tile, screen_rect.topleft)

            elif tile == "~":  # lava
                t = pygame.time.get_ticks() / 350

                for i in range(TILE_SIZE):
                    wave = math.sin(t + i * 0.25) * 0.5 + 0.5
                    color = (
                        200 + int(55 * wave),
                        60 + int(40 * wave),
                        20
                    )
                    pygame.draw.line(
                        surface,
                        color,
                        (screen_rect.left, screen_rect.top + i),
                        (screen_rect.right, screen_rect.top + i)
                    )

                glow = pygame.Surface((TILE_SIZE, TILE_SIZE * 3), pygame.SRCALPHA)

                for i in range(glow.get_height()):
                    dist = abs(i - glow.get_height() // 2) / (glow.get_height() // 2)
                    intensity = max(0, 1 - dist ** 2)
                    pygame.draw.line(
                        glow,
                        (
                            int(255 * intensity),
                            int(60 * intensity),
                            int(20 * intensity),
                            int(120 * intensity)
                        ),
                        (0, i),
                        (TILE_SIZE, i)
                    )

                surface.blit(
                    glow,
                    (screen_rect.left, screen_rect.centery - glow.get_height() // 2),
                    special_flags=pygame.BLEND_RGBA_ADD
                )

            elif tile == "^":  # spike
                pygame.draw.polygon(
                    surface,
                    (180, 180, 180),
                    [
                        (screen_rect.left, screen_rect.bottom),
                        (screen_rect.centerx, screen_rect.top),
                        (screen_rect.right, screen_rect.bottom),
                    ]
                )
            
            elif tile == "C":
                pygame.draw.rect(surface, (255, 215, 0), screen_rect)