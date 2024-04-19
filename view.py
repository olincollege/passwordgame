import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FONT_NAME = pygame.font.match_font("arial")
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)

class GameView:
    def __init__(self, model):
        self.model = model
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(FONT_NAME, size)
        text_surface = font.render(text, True, TEXT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        y = 50
        for message in self.model.messages:
            self.draw_text(message, 24, SCREEN_WIDTH // 2, y)
            y += 30
        self.draw_text(
            f"Current password: {self.model.password}",
            24,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 50,
        )
        pygame.display.flip()
