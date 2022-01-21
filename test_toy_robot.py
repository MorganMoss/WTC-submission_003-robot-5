import unittest
from unittest import mock
from io import StringIO
from command_handling.command_handling import CommandHandler
from command_handling.commands import Commands
import maze.empty_maze as Maze
from test_base import captured_io
from toy_robot import ToyRobot
from world.text.world import World


class TestToyRobot(unittest.TestCase):
    robby = ToyRobot()

    def test_say_message(self):
        with captured_io(StringIO()) as (out, err): 
            self.robby.robot_say_message("Message", "Start", "End")
        output = out.getvalue()
        self.assertEqual(output, "StartMessageEnd")
        with captured_io(StringIO()) as (out, err): 
            self.robby.robot_say_message("Message", end = "End")
        output = out.getvalue()
        self.assertEqual(output, "MessageEnd")
        with captured_io(StringIO()) as (out, err): 
            self.robby.robot_say_message("Message", start = "Start")
        output = out.getvalue()
        self.assertEqual(output, "StartMessage\n")


    def test_get_name(self):
        with captured_io(StringIO('ROBBY\n')) as (out, err):
            self.robby.robot_get_name()
        output = out.getvalue().strip()
        self.assertEqual("What do you want to name your robot?", output)
        self.assertEqual(self.robby.name, "ROBBY")
        

    @mock.patch.object(ToyRobot, "robot_get_name")
    @mock.patch.object(ToyRobot, "robot_say_message")
    def test_start(self, mock1, mock2):
        with captured_io(StringIO("ROBBY")) as (out, err):
            self.robby.start()
            mock1.assert_called()
            mock2.assert_called()

    @mock.patch.object(Commands, "exec_command")
    def test_cmd(self, mock):
        with captured_io(StringIO("oFf")) as (out, err):
            self.robby.cmd(World(Maze),Commands(),CommandHandler(Commands().command_dict))
            mock.assert_called()
            

if __name__ == '__main__':
    unittest.main()
