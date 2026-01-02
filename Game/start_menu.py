import pygame
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FONT_PATH = os.path.join(BASE_DIR, "fonts", "Micro5-Regular.ttf")

class StartMenu:
    def __init__(self, screen, screenWidth, screenHeight):
        self.screen = screen
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        self.title_font = pygame.font.Font(FONT_PATH, 64)
        self.menu_font = pygame.font.Font(FONT_PATH, 32)
        self.creator_font = pygame.font.Font(FONT_PATH, 24)

        self.bg_color = (242, 224, 172)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "start"
            if event.key == pygame.K_ESCAPE:
                return "quit"
        return None

    def draw(self):
        self.screen.fill(self.bg_color)

        title = self.title_font.render("WELCOME!", True, (255, 255, 255))
        subtitle = self.menu_font.render("Press Enter to Start", False, (180, 180, 180))
        quit_text = self.menu_font.render("Press ESC to Quit", False, (120, 120, 120))
        creator_text = self.creator_font.render("By Evelyn.....", False, (0, 0, 0))

        center_x = self.screenWidth // 2
        center_y = self.screenHeight // 2

        self.screen.blit(title, title.get_rect(center=(center_x, center_y - 80)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(center_x, center_y)))
        self.screen.blit(quit_text, quit_text.get_rect(center=(center_x, center_y + 40)))
        self.screen.blit(creator_text, creator_text.get_rect(center=(center_x, center_y + 200)))