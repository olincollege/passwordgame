if __name__ == "__main__":
    model = GameModel()
    view = GameView(model)
    controller = GameController(model, view)
    controller.run()
