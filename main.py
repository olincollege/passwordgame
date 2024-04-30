"""
Main module for initiating the game application.

This module sets up the game environment, initializing the
model, view, and controller
components of the game. It acts as the entry point of
the application, tying together
the game logic, user interface, and control flow.
Upon execution, this module
kicks off the game loop allowing users to interact with the game.

Classes:
    GameModel: Manages the game's state and logic.
    GameView: Handles rendering of the game
        graphics and user interface.
    GameController: Controls the flow of the game,
        processing user input and updating the model and view.

The game starts by creating instances of the GameModel,
GameView, and GameController, then
invoking the game loop through the controller.
"""

from model import GameModel
from view import GameView
from controller import GameController

if __name__ == "__main__":
    model = GameModel()
    view = GameView(model)
    controller = GameController(model, view)
    controller.run()
