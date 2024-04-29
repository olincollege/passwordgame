import unittest
from unittest.mock import Mock, patch
from controller import GameController
from model import GameModel
from view import GameView

class TestGameModel(unittest.TestCase):
    def setUp(self):
        """Set up a new game model for each test."""
        self.model = GameModel()

    def test_rule_min_length(self):
        """Test minimum length rule."""
        self.assertFalse(self.model.rule_min_length("abc"))
        self.assertTrue(self.model.rule_min_length("abcde"))

    def test_rule_include_numbers(self):
        """Test the rule that checks for at least one digit."""
        self.assertFalse(self.model.rule_include_numbers("abcdef"))
        self.assertTrue(self.model.rule_include_numbers("abc1"))

    def test_rule_include_uppercase(self):
        """Test the rule for at least one uppercase letter."""
        self.assertFalse(self.model.rule_include_uppercase("abc"))
        self.assertTrue(self.model.rule_include_uppercase("Abc"))

    def test_rule_include_special_character(self):
        """Test the rule for at least one special character."""
        self.assertFalse(self.model.rule_include_special_character("abc"))
        self.assertTrue(self.model.rule_include_special_character("abc!"))

    def test_rule_include_fibonacci(self):
        """Test the rule for including a Fibonacci number."""
        self.assertFalse(self.model.rule_include_fibonacci("abc"))
        self.assertTrue(self.model.rule_include_fibonacci("abc8"))

    def test_rule_include_morse(self):
        """Test the rule for including Morse code characters."""
        self.assertFalse(self.model.rule_include_morse("abc"))
        self.assertTrue(self.model.rule_include_morse("abc-."))

    def test_rule_include_month(self):
        """Test the rule for including a month name."""
        self.assertFalse(self.model.rule_include_month("abc"))
        self.assertTrue(self.model.rule_include_month("january"))

    def test_rule_include_roman_numeral(self):
        """Test the rule for including a Roman numeral."""
        self.assertFalse(self.model.rule_include_roman_numeral("abc"))
        self.assertTrue(self.model.rule_include_roman_numeral("abcX"))

    def test_rule_sum_prime(self):
        """Test the rule for the sum of digits being a prime number."""
        self.assertFalse(self.model.rule_sum_prime("abc123"))  # 1+2+3 = 6, not prime
        self.assertTrue(self.model.rule_sum_prime("abc35"))   # 3+5 = 8, not prime

    def test_rule_chess_sicilian_defense(self):
        """Test the rule for including 'c5' chess move."""
        self.assertFalse(self.model.rule_chess_sicilian_defense("abc"))
        self.assertTrue(self.model.rule_chess_sicilian_defense("abc c5"))

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
