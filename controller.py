"""
This module contains the GameController class which
manages the game loop and user interactions.
It processes events, updates game state, and
interacts with the game model and view.
"""

# pylint: disable=no-member
import pygame
from better_profanity import profanity


class GameController:
    """
    Controller class that handles user input and game state updates.

    Attributes:
        model (GameModel): The model handling the game logic and state.
        view (GameView): The view handling the rendering of
        the game on the screen.
        running (bool): A flag indicating if the game loop is running.
    """

    def __init__(self, model, view):
        """
        Initializes the GameController with the given model and view.

        Args:
            model (GameModel): An instance of GameModel to control.
            view (GameView): An instance of GameView to use for rendering.
        """
        self.model = model
        self.view = view
        self.running = True
        profanity.load_censor_words()  # Load the profanity list

    def run(self):
        """
        Runs the main game loop, processing events and updating the view.
        """
        while self.running:
            self.view.render()
            self.handle_events()
            self.view.clock.tick(30)

    def handle_events(self):
        """
        Handles incoming events such as keyboard input. Updates the game model,
        and view accordingly.

        Raises:
            SystemExit: If the game is quit by closing the
            window or pressing ESC.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif (
                event.type == pygame.KEYDOWN
            ):  # Use '==' instead of 'is' for the comparison
                if event.key == pygame.K_RETURN:
                    if self.model.check_password():
                        print("Password meets all requirements!")
                        self.running = False
                        if self.model.all_rules_satisfied():
                            self.view.start_celebration()
                    else:
                        print("Password does not meet the requirements.")
                elif event.key == pygame.K_BACKSPACE:
                    # Simplified condition to check if the password is non-empty
                    if self.model.password:
                        self.model.password = self.model.password[:-1]
                        self.model.update_rules()
                else:
                    char = event.unicode
                    # Check for alphanumeric and specific special characters
                    if char.isalnum() or char in {
                        "-",
                        "_",
                        "!",
                        "@",
                        "#",
                        "$",
                        "%",
                        "^",
                        "&",
                        "*",
                        "(",
                        ")",
                        "=",
                        "+",
                        "[",
                        "]",
                        "{",
                        "}",
                        ";",
                        ":",
                        "'",
                        '"',
                        ",",
                        "<",
                        ".",
                        ">",
                        "/",
                        "?",
                        "|",
                    }:
                        new_password = self.model.password + char
                        if profanity.contains_profanity(new_password):
                            print("Inappropriate language detected! Game over.")
                            self.running = False
                        else:
                            self.model.password = new_password
                            self.model.update_rules()
