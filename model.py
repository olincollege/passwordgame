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