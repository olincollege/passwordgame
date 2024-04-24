import pygame
import sys
import textwrap

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FONT_NAME = pygame.font.match_font("arial")
BACKGROUND_COLOR = (250, 248, 239)
TEXT_COLOR = (0, 0, 0)
INPUT_BOX_COLOR = (255, 255, 255)
RULE_MET_COLOR = (153, 204, 0)
RULE_NOT_MET_COLOR = (255, 77, 77)
RULE_RECT_WIDTH = 400
LINE_SPACING = 4


class GameView:
    def __init__(self, model):
        self.model = model
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, 24)
        self.input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 100, 300, 50)

    def draw_text_wrapped(self, text, rect, color):
        y_offset = 0
        for line in textwrap.wrap(text, width=25):
            line_surface = self.font.render(line, True, color)
            self.screen.blit(line_surface, (rect.x + 5, rect.y + y_offset))
            y_offset += self.font.get_linesize() + LINE_SPACING

    def draw_input_box(self):
        pygame.draw.rect(self.screen, INPUT_BOX_COLOR, self.input_box, 0)
        self.draw_text_wrapped(self.model.password, self.input_box, TEXT_COLOR)

    def draw_rules(self):
        # Split rules into satisfied and unsatisfied
        unsatisfied_rules = [
            (message, rule)
            for message, rule in zip(self.model.messages, self.model.rules)
            if not rule(self.model.password)
        ]
        satisfied_rules = [
            (message, rule)
            for message, rule in zip(self.model.messages, self.model.rules)
            if rule(self.model.password)
        ]

        y = self.input_box.bottom + 20
        # Draw unsatisfied rules first
        for message, rule_method in unsatisfied_rules:
            rule_color = RULE_NOT_MET_COLOR
            text_height = len(textwrap.wrap(message, width=25)) * (
                self.font.get_linesize() + LINE_SPACING
            )
            rule_rect = pygame.Rect(
                self.input_box.left, y, RULE_RECT_WIDTH, text_height + 10
            )
            pygame.draw.rect(self.screen, rule_color, rule_rect)
            self.draw_text_wrapped(message, rule_rect, TEXT_COLOR)
            y += text_height + 15

        # Then draw satisfied rules
        for message, rule_method in satisfied_rules:
            rule_color = RULE_MET_COLOR
            text_height = len(textwrap.wrap(message, width=25)) * (
                self.font.get_linesize() + LINE_SPACING
            )
            rule_rect = pygame.Rect(
                self.input_box.left, y, RULE_RECT_WIDTH, text_height + 10
            )
            pygame.draw.rect(self.screen, rule_color, rule_rect)
            self.draw_text_wrapped(message, rule_rect, TEXT_COLOR)
            y += text_height + 15

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_text_wrapped(
            "The Password Game",
            pygame.Rect(SCREEN_WIDTH // 2 - 150, 20, 300, 50),
            TEXT_COLOR,
        )
        self.draw_input_box()
        self.draw_rules()
        pygame.display.flip()
