import unittest
from unittest.mock import Mock, patch
import pygame
from model import GameModel
from controller import GameController
from view import GameView

#Unit tests for Model
class TestGameModel(unittest.TestCase):
    def setUp(self):
        """Set up a new game model for each test."""
        self.model = GameModel()

    def test_password_initially_empty(self):
        """Test that the initial password is an empty string."""
        self.assertEqual(self.model.password, "")

    def test_update_rules_initial(self):
        """Test the initial state of rule updating."""
        self.model.update_rules()
        self.assertFalse(self.model.all_rules_satisfied)
        self.assertEqual(self.model.current_rule_index, 0)

    def test_check_password_empty(self):
        """Test check_password on an initially empty password."""
        self.assertFalse(self.model.check_password())

    # Additional scenarios for existing tests
    def test_rule_min_length_edge_case(self):
        """Test minimum length rule at exactly 5 characters."""
        self.assertTrue(self.model.rule_min_length("12345"))

    def test_rule_include_numbers_edge_case(self):
        """Test for a password containing numbers only."""
        self.assertTrue(self.model.rule_include_numbers("1234567890"))

    def test_rule_include_uppercase_multiple(self):
        """Test for multiple uppercase letters."""
        self.assertTrue(self.model.rule_include_uppercase("ABC"))

    def test_rule_include_special_character_edge_cases(self):
        """Test for each special character defined."""
        special_chars = "!@#$%^&*()_+-=[]{};:',<.>/?"
        for char in special_chars:
            self.assertTrue(self.model.rule_include_special_character(f"abc{char}def"))

    def test_rule_include_fibonacci_end_number(self):
        """Test including a Fibonacci number at the end of the string."""
        self.assertTrue(self.model.rule_include_fibonacci("password144"))

    def test_rule_include_month_case_insensitivity(self):
        """Test for case insensitivity in month inclusion."""
        self.assertTrue(self.model.rule_include_month("We met in OCTOBER"))

    def test_rule_include_roman_numeral_multiple(self):
        """Test for multiple Roman numerals."""
        self.assertTrue(self.model.rule_include_roman_numeral("I have VI apples"))

    def test_rule_sum_prime_large_numbers(self):
        """Test prime rule with larger numbers summing to a prime."""
        self.assertTrue(self.model.rule_sum_prime("abc978977")) 

    def test_rule_chess_sicilian_defense_variation(self):
        """Test for variations of the Sicilian Defense rule."""
        self.assertTrue(self.model.rule_chess_sicilian_defense("e4 c5 d6"))

    def test_next_look_and_say_valid(self):
        """Test if the Look-and-Say rule correctly predicts the next sequence."""
        self.model.last_look_and_say = '1' 
        self.model.next_look_and_say = self.model.next_look_and_say_sequence('1')
        expected_next = '11' 
        self.assertEqual(self.model.next_look_and_say, expected_next, msg=f"Expected {expected_next}, got {self.model.next_look_and_say}")

#Unit tests for Controller
class TestGameController(unittest.TestCase):
    def setUp(self):
        """Set up mock model and view, and instantiate the controller."""
        self.model = Mock(spec=GameModel)
        self.view = Mock(spec=GameView)
        self.controller = GameController(self.model, self.view)

    def test_init(self):
        """Test controller initialization."""
        self.assertTrue(self.controller.running)
        self.assertEqual(self.controller.model, self.model)
        self.assertEqual(self.controller.view, self.view)

    @patch('pygame.event.get')
    def test_handle_events_quit(self, mock_event_get):
        """Test handling the QUIT event."""
        mock_event_get.return_value = [Mock(type=pygame.QUIT)]
        self.controller.handle_events()
        self.assertFalse(self.controller.running)

    @patch('pygame.event.get')
    def test_handle_events_keydown(self, mock_event_get):
        """Test handling the KEYDOWN event."""
        mock_event = Mock(type=pygame.KEYDOWN)
        mock_event.key = pygame.K_RETURN
        mock_event_get.return_value = [mock_event]
        self.model.check_password.return_value = False
        self.controller.handle_events()
        self.model.check_password.assert_called_once()

# Unit tests for View
class TestGameView(unittest.TestCase):
    def setUp(self):
        """Set up a mock model and instantiate the view."""
        self.model = Mock(spec=GameModel)
        self.view = GameView(self.model)

    def test_init(self):
        """Test view initialization and attributes."""
        self.assertEqual(self.view.model, self.model)
        self.assertIsNotNone(self.view.screen)
        self.assertIsNotNone(self.view.clock)
        self.assertIsNotNone(self.view.font)

if __name__ == "__main__":
    unittest.main()
