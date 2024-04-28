import pygame
import sys
import textwrap
import random

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
CONGRATULATIONS_COLOR = (255, 223, 0)


class GameView:
    """
    The view component of the game that handles all visual rendering.

    Attributes:
        model (GameModel): The game's model with which the view interacts.
        screen (pygame.Surface): The main display surface for the game.
        clock (pygame.time.Clock): A clock object to manage frame rate.
        font (pygame.font.Font): The font used for rendering text.
        input_box (pygame.Rect): The input box where the user's password is displayed.
        cursor_visible (bool): Indicates if the cursor is currently visible.
        cursor_timer (int): Counts the time for cursor visibility toggling.
        cursor_interval (int): The interval at which the cursor visibility toggles.
        congratulations (bool): Indicates if the celebration sequence should run.
        confetti (list): A list of confetti parameters for the celebration sequence.
    """

    def __init__(self, model):
        """
        Initializes the GameView with the given model and sets up the display surface.

        Args:
            model (GameModel): The game's model that contains the game state.
        """
        self.model = model
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(FONT_NAME, 24)
        self.input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, 100, 300, 50)
        self.cursor_visible = True  # Cursor visibility flag
        self.cursor_timer = 0  # Timer for cursor blinking
        self.cursor_interval = 500  # Cursor blink interval in milliseconds
        self.congratulations = False
        self.confetti = []

    def draw_text_wrapped(self, text, rect, color):
        """
        Draws text within a given rectangle, wrapping it to fit within the width.

        Args:
            text (str): The text to be drawn.
            rect (pygame.Rect): The rectangle area where the text will be drawn.
            color (tuple): The color of the text.
        """
        y_offset = 0
        for line in textwrap.wrap(text, width=25):
            line_surface = self.font.render(line, True, color)
            self.screen.blit(line_surface, (rect.x + 5, rect.y + y_offset))
            y_offset += self.font.get_linesize() + LINE_SPACING

    def draw_input_box(self):
        """
        Draws the input box where the user's password is displayed.
        """
        pygame.draw.rect(self.screen, INPUT_BOX_COLOR, self.input_box, 0)
        text_surface = self.font.render(self.model.password, True, TEXT_COLOR)
        self.screen.blit(
            text_surface, (self.input_box.x + 5, self.input_box.y + 10)
        )
        if self.cursor_visible:
            cursor_x = self.input_box.x + 5 + text_surface.get_width()
            cursor_y = self.input_box.y + 10
            cursor_height = text_surface.get_height()
            pygame.draw.line(
                self.screen,
                TEXT_COLOR,
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_height),
            )

    def draw_rules(self):
        """
        Draws the game rules, highlighting satisfied rules and the current active rule.
        """
        # Check if all rules are satisfied before drawing
        if self.model.all_rules_satisfied:
            self.start_celebration()
            return
        # Clear any previously drawn rules before drawing new ones
        rules_start_y = self.input_box.bottom + 40
        rules_background_rect = pygame.Rect(
            0, rules_start_y, SCREEN_WIDTH, SCREEN_HEIGHT - rules_start_y
        )
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, rules_background_rect)

        # First, draw the "Password Game" title
        self.draw_text_wrapped(
            "The Password Game",
            pygame.Rect(0, 20, SCREEN_WIDTH, 100),
            TEXT_COLOR,
        )

        # Draw the unsatisfied rule at the top
        if self.model.current_rule_index < len(self.model.rules):
            message = self.model.messages[self.model.current_rule_index]
            rule_color = (
                RULE_NOT_MET_COLOR
                if not self.model.rules[self.model.current_rule_index](
                    self.model.password
                )
                else RULE_MET_COLOR
            )
            self.draw_rule(message, rules_start_y, rule_color)

        # Draw satisfied rules in green below the current rule
        y_offset = (
            rules_start_y
            + self.get_text_height(
                self.model.messages[self.model.current_rule_index]
            )
            + 15
        )
        for index in self.model.satisfied_rules:
            if index != self.model.current_rule_index:
                message = self.model.messages[index]
                self.draw_rule(message, y_offset, RULE_MET_COLOR)
                y_offset += self.get_text_height(message) + 15

    def draw_rule(self, text, y, color):
        """
        Draws a single rule with the specified text, vertical position, and color.

        Args:
            text (str): The text representing the rule.
            y (int): The y-coordinate for the top of the text.
            color (tuple): The background color of the rule's rectangle.
        """
        text_height = self.get_text_height(text)
        rule_rect = pygame.Rect(
            (SCREEN_WIDTH - RULE_RECT_WIDTH) / 2,
            y,
            RULE_RECT_WIDTH,
            text_height + 10,
        )
        pygame.draw.rect(self.screen, color, rule_rect)
        self.draw_text_wrapped(text, rule_rect, TEXT_COLOR)

    def get_text_height(self, text):
        """
        Calculates the height of wrapped text.

        Args:
            text (str): The text to calculate the height for.

        Returns:
            int: The total height of the wrapped text.
        """
        return len(textwrap.wrap(text, width=25)) * (
            self.font.get_linesize() + LINE_SPACING
        )

    def start_celebration(self):
        """
        Initiates the celebration sequence by generating confetti and setting the
        flag to start the celebration.
        """
        self.congratulations = True
        self.confetti_count = 50  # Set a limit to the number of confetti pieces
        for _ in range(self.confetti_count):  # Generate confetti particles
            self.confetti.append(
                (
                    random.randint(0, SCREEN_WIDTH),
                    random.randint(0, SCREEN_HEIGHT),
                    random.choice(
                        [
                            CONGRATULATIONS_COLOR,
                            (255, 0, 0),
                            (0, 255, 0),
                            (0, 0, 255),
                        ]
                    ),
                    random.randint(5, 10),  # Random size for confetti
                )
            )

    def draw_celebration(self):
        """
        Draws the celebration sequence with confetti and a congratulatory message.
        """
        # Draw confetti particles
        for _ in range(50):
            for x, y, color, size in self.confetti:
                pygame.draw.circle(self.screen, color, (x, y), size)

            # Draw "Congratulations" message on top of the confetti
            congratulations_font = pygame.font.Font(
                FONT_NAME, 48
            )  # Larger font for the message
            congratulations_text = congratulations_font.render(
                "Congratulations! You've won!",
                True,
                (0, 0, 0),  # Use a dark color for visibility
            )
            # Position the text in the center of the screen
            text_rect = congratulations_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            pygame.draw.rect(
                self.screen, BACKGROUND_COLOR, text_rect
            )  # Draw a background rect for the text
            self.screen.blit(congratulations_text, text_rect)

    def render(self):
        """
        Renders the entire view, including the input box, rules, and the celebration
        sequence if all rules are satisfied.
        """
        self.screen.fill(BACKGROUND_COLOR)
        if self.congratulations:
            self.draw_celebration()
        else:
            self.draw_input_box()
            self.draw_rules()
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_input_box()
        self.draw_rules()
        if self.congratulations:
            self.draw_celebration()
        # Cursor timing logic for blinking
        self.cursor_timer += self.clock.get_time()
        if self.cursor_timer >= self.cursor_interval:
            self.cursor_timer %= self.cursor_interval
            self.cursor_visible = not self.cursor_visible
        pygame.display.flip()
        self.clock.tick(30)
