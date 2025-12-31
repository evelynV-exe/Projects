import pygame
import time
import os

pygame.font.init()

BASE_DIR = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_DIR, "fonts", "Micro5-Regular.ttf")
font = pygame.font.Font(FONT_PATH, 18)

#character
class Player():
    def __init__(self, x, y, width=15, height=15):
        self.rect = pygame.Rect(x, y, width, height)

        #movement
        self.velocity_y = 0
        self.gravity = 0.2
        self.jump_strength = -4

        #horizontal movement
        self.speed = 2

        #jump system
        self.jump_count = 0
        self.max_jumps = 2
        self.lastJump_time = 0
        self.cooldown = 2

        #state
        self.on_ground = False
        

    def update(self, keys, tiles, screenWidth, screenHeight):
        self.on_ground = False

        #horizontal movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            self._horizontal_collision(tiles)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            self._horizontal_collision(tiles)

        #gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        self._vertical_collision(tiles)

        #prevent leaving screen horizontally
        if self.rect.left <  0:
            self.rect.left = 0
        elif self.rect.right > screenWidth:
            self.rect.right = screenWidth
        
        #prevent going above the screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

        #Dead
        if self.rect.top > screenHeight:
            return "dead"
        return None

    def jump(self):
        current_time = time.time()

        #check cooldown
        if current_time - self.lastJump_time < self.cooldown:
            return
        
        if self.jump_count < self.max_jumps:
            self.velocity_y = self.jump_strength
            self.jump_count += 1

            #the second jump
            if self.jump_count == self.max_jumps:
                self.lastJump_time = current_time

    def _horizontal_collision(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.rect.x < tile.x:
                    self.rect.right = tile.left
                else:
                    self.rect.left = tile.right
    
    def _vertical_collision(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.velocity_y > 0:
                    self.rect.bottom = tile.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jump_count = 0
                elif self.velocity_y < 0:
                    self.rect.top = tile.bottom
                    self.velocity_y = 0

    #player
    def draw(self, surface):
        pygame.draw.rect(surface, (50, 168, 82), self.rect)

    #the cooldown bar
    def draw_cooldown(self, surface, screenWidth):
        bar_w = 200
        bar_h = 22
        margin = 15
        
        bar_x = screenWidth - bar_w - margin
        bar_y = 15

        bar_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)

        elapsed = time.time() - self.lastJump_time
        progress = min(elapsed / self.cooldown, 1.0)

        pygame.draw.rect(surface, (220, 220, 220), bar_rect)
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, int(bar_w * progress), bar_h))

        if progress < 1.0:
            text = font.render("Cooldown...", True, (0, 0, 0))
        else:
            text = font.render("Jump Ready!", True, (0, 0, 0))
        text_rect = text.get_rect(center=bar_rect.center)
        surface.blit(text, text_rect)
