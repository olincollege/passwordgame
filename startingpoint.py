import pygame
import sys

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
FONT_NAME = pygame.font.match_font("arial")
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)


# Model
class GameModel:
    def __init__(self):
        self.password = ""
        self.rules = [self.rule_min_length]
        self.current_rule_index = 0
        self.messages = ["Password must be at least 5 characters long."]

    def rule_min_length(self, password):
        return len(password) >= 5

    def rule_include_numbers(self, password):
        return sum(c.isdigit() for c in password) >= 2

    def update_rules(self):
        if self.current_rule_index == 0 and self.rule_min_length(self.password):
            self.rules.append(self.rule_include_numbers)
            self.messages.append("Password must include at least 2 numbers.")
            self.current_rule_index += 1
        # Add more rules and their messages here

    def check_password(self):
        return all(rule(self.password) for rule in self.rules)


# View
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


# Controller
class GameController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = True

    def run(self):
        while self.running:
            self.view.render()
            self.handle_events()
            self.view.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.model.check_password():
                        print("Password meets all requirements!")
                        self.running = False
                    else:
                        print("Password does not meet the requirements.")
                elif event.key == pygame.K_BACKSPACE:
                    self.model.password = self.model.password[:-1]
                    self.model.update_rules()
                else:
                    char = pygame.key.name(event.key)
                    if char.isalnum() or char in {
                        "-",
                        "_",
                    }:  # Allow alphanumeric and specific characters
                        self.model.password += char
                        self.model.update_rules()


# Main function
if __name__ == "__main__":
    model = GameModel()
    view = GameView(model)
    controller = GameController(model, view)
    controller.run()
