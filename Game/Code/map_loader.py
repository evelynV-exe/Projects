import pygame

TILE_SIZE = 15

def load_map(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]
    
def solid(game_map):
    tiles = []
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if tile == "1":
                tiles.append(pygame.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return tiles

def draw_map(surface, game_map):
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            if tile == "1":
                pygame.draw.rect(surface, (70, 70, 70), 
                                 (col_index * TILE_SIZE, row_index * TILE_SIZE,
                                  TILE_SIZE, TILE_SIZE))
