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