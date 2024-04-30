"""
Model module for the game, responsible for
handling game logic and state.

This module defines the GameModel class,
which encapsulates all the data needed
for the game, including player inputs, game rules,
and game status. It manages
the validation of user input against defined rules,
tracking rule satisfaction,
and maintaining the state of the game as it progresses.

Classes:
    GameModel: Holds and manages the state of the game
    including the user's password,
    the validation rules, messages associated with each rule,
    and the current
    state of rule satisfaction.

The GameModel class is designed to be interacted with by
the GameController,
which uses its methods to update the game state based
on user actions, and
by the GameView for displaying the current state of the game.
"""

from math import sqrt, isqrt
import random
from sympy import isprime

class GameModel:
    """
    The model for the password validation game which enforces
    various password rules.

    Attributes:
        password (str): The user's current input attempting
            to satisfy all password rules.
        rules (list): A list of methods that represent the rules
            the password must satisfy.
        messages (list): A list of strings representing messages
            for each rule to display.
        current_rule_index (int): The index of the currently active rule.
        satisfied_rules (list): A list of indices representing rules
            that have been satisfied.
        all_rules_satisfied (bool): Indicates if all rules have been satisfied.
        last_look_and_say (str): The last sequence in the look-and-say series.
        next_look_and_say (str): The next sequence in the look-and-say
            series that needs to be guessed.
    """

    def __init__(self):
        """
        Initializes the GameModel with a set of
        password validation rules and messages
        associated with each rule. Also initializes
        the state for tracking rule satisfaction
        and the look-and-say sequence for the current game session.

        """
        self.password = ""
        self.init_look_and_say()
        self.rules = [
            self.rule_min_length,
            self.rule_include_numbers,
            self.rule_include_uppercase,
            self.rule_include_special_character,
            self.rule_include_fibonacci,
            self.rule_include_morse,
            self.rule_include_month,
            lambda password: self.next_look_and_say in password,
            self.rule_include_roman_numeral,
            self.rule_sum_prime,
            self.rule_chess_sicilian_defense,
        ]
        self.messages = [
            "Password must be at least 5 characters long.",
            "Password must include a number.",
            "Password must include an uppercase letter.",
            "Password must include a special character.",
            "Password must include a number from the Fibonacci sequence.",
            "Include a Morse code character.",
            "Your password must include a month of the year.",
            "Enter the next sequence in Look-and-Say after {self.last_look_and_say}",
            "Your password must include a Roman numeral.",
            "The sum of all numbers in the password must be a prime number.",
            "Respond to e4 with the Sicilian Defense.",
        ]
        self.current_rule_index = 0  # Initialize with the first rule
        self.satisfied_rules = []  # List to store indices of satisfied rules
        self.all_rules_satisfied = False

    def update_rules(self):
        """
        Re-evaluates all rules based on the current password.
        Updates the list of satisfied rules
        and determines the current rule index.
        Also sets the flag for all rules being satisfied.
        """
        # Check all rules based on the current
        # password and update their satisfaction status
        self.satisfied_rules = []
        self.current_rule_index = 0
        for index, rule in enumerate(self.rules):
            if rule(self.password):
                self.satisfied_rules.append(index)
            else:
                # If any rule is not satisfied,
                # we set it as the current rule to break the loop
                self.current_rule_index = index
                break

        # Set 'all_rules_satisfied' to True if all rules have been met
        self.all_rules_satisfied = len(self.satisfied_rules) == len(self.rules)

    def check_password(self):
        """
        Checks if the current password satisfies all the active rules.

        Returns:
            bool: True if all rules are satisfied, otherwise False.
        """
        # Check if all rules are satisfied
        return self.current_rule_index >= len(self.rules)

    def rule_min_length(self, password):
        """
        Validates that the password meets the minimum length requirement.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password meets the
                minimum length, False otherwise.
        """
        return len(password) >= 5

    def rule_include_numbers(self, password):
        """
        Validates that the password contains at least one digit.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains a digit, False otherwise.
        """
        return any(c.isdigit() for c in password)

    def rule_include_uppercase(self, password):
        """
        Validates that the password contains at least one uppercase letter.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains an uppercase letter,
            False otherwise.
        """
        return any(c.isupper() for c in password)

    def rule_include_special_character(self, password):
        """
        Validates that the password contains at least one special character.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains a special character,
            False otherwise.
        """
        return any(not c.isalnum() for c in password)

    def rule_include_fibonacci(self, password):
        """
        Validates that the password contains a
        number from the Fibonacci sequence.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains a
            Fibonacci number, False otherwise.
        """
        fib_nums = {
            0,
            1,
            1,
            2,
            3,
            5,
            8,
            13,
            21,
            34,
            55,
            89,
            144,
            233,
            377,
            610,
            987,
        }
        return any(str(num) in password for num in fib_nums)

    def rule_include_morse(self, password):
        """
        Validates that the password contains at least one
        Morse code character ('.' or '-').

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains a Morse code character,
            False otherwise.
        """
        return "." in password or "-" in password

    def rule_include_month(self, password):
        """
        Validates that the password contains the name of a month.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains a month, False otherwise.
        """
        months = {
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
            "july",
            "august",
            "september",
            "october",
            "november",
            "december",
        }
        return any(month in password.lower() for month in months)

    def rule_include_roman_numeral(self, password):
        """
        Validates that the password contains at least one Roman numeral.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains
                a Roman numeral, False otherwise.
        """
        roman_numerals = {"I", "V", "X", "L", "C", "D", "M"}
        return any(numeral in password for numeral in roman_numerals)

    def rule_sum_prime(self, password):
        """
        Validates that the sum of all digits in the password is a prime number.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the sum of digits is a prime number, False otherwise.
        """
        total = sum(int(c) for c in password if c.isdigit())
        return isprime(total)

    def rule_chess_sicilian_defense(self, password):
        """
        Validates that the password contains the move 'c5',
        a response to the chess opening move 'e4'.

        Args:
            password (str): The password to validate.

        Returns:
            bool: True if the password contains the move 'c5', False otherwise.
        """
        # Check if the password includes the move "c5"
        return "c5" in password

    def init_look_and_say(self):
        """
        Initializes the look-and-say sequence by determining
        a random sequence length
        and generating the required sequence as per the game rules.

        Raises:
            ValueError: If the generated sequence does
                not meet expected criteria.
        """
        # Randomly determine the number of steps (e.g., between 3 and 6)
        num_steps = random.randint(3, 6)
        self.last_look_and_say = "1"
        for _ in range(num_steps):
            self.last_look_and_say = self.next_look_and_say_sequence(
                self.last_look_and_say
            )
        self.next_look_and_say = self.next_look_and_say_sequence(
            self.last_look_and_say
        )

    @staticmethod
    def next_look_and_say_sequence(sequencex):
        """
        Calculates the next sequence in the look-and-say
        series based on the given input sequence.

        Args:
            sequencex (str): The current sequence from which
                the next one will be generated.

        Returns:
            str: The next sequence in the look-and-say series.
        """
        result, i = [], 0
        while i < len(sequencex):
            count = 1
            while i + 1 < len(sequencex) and sequencex[i] == sequencex[i + 1]:
                i += 1
                count += 1
            result.append(str(count) + sequencex[i])
            i += 1
        return "".join(result)
