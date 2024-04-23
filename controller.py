import pygame


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
                        # self.running = False
                        self.model.update_rules()
                        if self.model.current_rule_index >= len(
                            self.model.rules
                        ):
                            print("All rules met, game complete!")
                            self.running = False
                        # if not self.running:
                        #     continue
                    else:
                        print("Password does not meet the requirements.")
                elif event.key == pygame.K_BACKSPACE:
                    self.model.password = self.model.password[:-1]
                    # self.model.update_rules()
                else:
                    char = event.unicode
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
                    }:
                        self.model.password += char
                        # self.model.update_rules()
                if not self.model.check_password():
                    print("Password does not currently meet the requirements.")
