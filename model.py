import re
from math import sqrt, isqrt
from sympy import isprime

class GameModel:
    def __init__(self):
        self.password = ""
        self.rules = [self.rule_min_length]
        self.current_rule_index = 0
        self.messages = ["Password must be at least 5 characters long."]

    def rule_min_length(self, password):
        return len(password) >= 5

    def rule_include_numbers(self, password):
        return sum(c.isdigit() for c in password) >= 1

    def rule_include_uppercase(self, password):
        return any(c.isupper() for c in password)

    def rule_include_special_character(self, password):
        return any(not c.isalnum() for c in password)
    
    def rule_include_fibonacci(self, password):
        fib_nums = {0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987}
        return any(str(num) in password for num in fib_nums)

    def rule_include_morse(self, password):
        # Morse code characters are '.', '-'
        return '.' in password or '-' in password
    
    def rule_include_month(self, password):
        months = {"january", "february", "march", "april", "may", "june",
                  "july", "august", "september", "october", "november", "december"}
        return any(month in password.lower() for month in months)

    def rule_include_roman_numeral(self, password):
        roman_numerals = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
        return any(numeral in password for numeral in roman_numerals)
    
    def rule_sum_prime(self, password):
        total = sum(int(c) for c in password if c.isdigit())
        return isprime(total)

    def update_rules(self):
        rule_methods = [
            (self.rule_include_numbers, "Password must include a number."),
            (self.rule_include_uppercase, "Password must include an uppercase letter."),
            (self.rule_include_special_character, "Password must include a special character."),
            (self.rule_include_fibonacci, "Password must include a number from the fibonacci sequence."),
            (self.rule_include_morse, "Include a Morse code character."),
            (self.rule_include_month, "Your password must include a month of the year."),
            (self.rule_include_roman_numeral, "Your password must include a Roman numeral."),
            (self.rule_sum_prime, "The sum of all numbers in the password must be a prime number."),
        ]

        # Automatically adds the next rule when the current is met
        if self.rules[-1](self.password):
            next_rule, message = rule_methods[self.current_rule_index]
            self.rules.append(next_rule)
            self.messages.append(message)
            self.current_rule_index += 1

    def check_password(self):
        return all(rule(self.password) for rule in self.rules)