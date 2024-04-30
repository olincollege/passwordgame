"""
Main module to launch the password game.

This module sets up the model, view, and controller
components and initiates the game loop.
"""

from model import GameModel
from view import GameView
from controller import GameController

if __name__ == "__main__":
    model = GameModel()
    view = GameView(model)
    controller = GameController(model, view)
    controller.run()
