import unittest
from io import StringIO
from test_base import captured_io
import math
from toy_robot.robot_base import BaseRobot

class TestBaseRobot(unittest.TestCase):
    base_robby = BaseRobot()

    def test_say_message(self):
        with captured_io(StringIO()) as (out, err): 
            self.base_robby.robot_say_message("Message", "Start", "End")
        output = out.getvalue()
        self.assertEqual(output, "StartMessageEnd")
        with captured_io(StringIO()) as (out, err): 
            self.base_robby.robot_say_message("Message", end = "End")
        output = out.getvalue()
        self.assertEqual(output, "MessageEnd")
        with captured_io(StringIO()) as (out, err): 
            self.base_robby.robot_say_message("Message", start = "Start")
        output = out.getvalue()
        self.assertEqual(output, "StartMessage\n")


    def test_get_name(self):
        with captured_io(StringIO('ROBBY\n')) as (out, err):
            self.base_robby.robot_get_name()
        output = out.getvalue().strip()
        self.assertEqual("What do you want to name your robot?", output)
        self.assertEqual(self.base_robby.name, "ROBBY")
        

if __name__ == '__main__':
    unittest.main()