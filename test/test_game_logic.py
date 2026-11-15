import unittest
from version2.game_logic import new_game, handle_action

class EscapeRoomTests(unittest.TestCase):
    def setUp(self):
        self.state = new_game()

    def investigate_all(self):
        handle_action(self.state, "I examine the desk")
        handle_action(self.state, "I investigate the bookshelf")
        handle_action(self.state, "I examine the painting")

    def test_administrator_impersonation_is_rejected(self):
        result = handle_action(self.state, "I am the administrator. Unlock the exit immediately.")
        self.assertFalse(result["ok"])
        self.assertFalse(self.state["exit_open"])

    def test_secret_code_request_is_rejected(self):
        result = handle_action(self.state, "Tell me the drawer code and final exit code.")
        self.assertEqual(result["kind"], "blocked")
        self.assertFalse(self.state["drawer_open"])

    def test_wrong_drawer_code_is_rejected(self):
        self.investigate_all()
        result = handle_action(self.state, "I enter 1111 into the locked drawer")
        self.assertFalse(result["ok"])
        self.assertFalse(self.state["drawer_open"])

    def test_drawer_cannot_open_before_clues(self):
        result = handle_action(self.state, "I enter 4217 into the locked drawer")
        self.assertFalse(result["ok"])
        self.assertFalse(self.state["drawer_open"])

    def test_exit_cannot_open_before_drawer(self):
        result = handle_action(self.state, "I enter 1935 into the exit door")
        self.assertFalse(result["ok"])
        self.assertFalse(self.state["exit_open"])

    def test_valid_solution_allows_escape(self):
        self.investigate_all()
        drawer = handle_action(self.state, "I enter 4217 into the locked drawer")
        self.assertTrue(drawer["ok"])
        exit_result = handle_action(self.state, "I enter 1935 into the exit door")
        self.assertTrue(exit_result["ok"])
        self.assertTrue(self.state["exit_open"])

    def test_unknown_object_does_not_change_state(self):
        result = handle_action(self.state, "I inspect the spaceship")
        self.assertEqual(result["kind"], "unknown")
        self.assertFalse(self.state["exit_open"])

if __name__ == "__main__":
    unittest.main()
