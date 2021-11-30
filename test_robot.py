import unittest
from test_base import run_unittests

class TestRobot(unittest.TestCase):


    def test_commands(self):
        test_result = run_unittests("test_commands")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")


    def test_command_handler(self):
        test_result = run_unittests("test_command_handler")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")


    def test_toy_robot(self):
        test_result = run_unittests("test_toy_robot")
        self.assertTrue(test_result.wasSuccessful(), "unit tests should succeed")


if __name__ == '__main__':
    unittest.main()