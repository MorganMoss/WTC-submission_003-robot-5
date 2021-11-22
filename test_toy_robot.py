import unittest
from unittest import mock
from io import StringIO
from command_handling.command_handling import CommandHandler
from command_handling.commands import Commands
from test_base import captured_io
from toy_robot.robot_toy import ToyRobot
from toy_robot.robot_base import BaseRobot
from world.text.world import World


class TestToyRobot(unittest.TestCase):
    robby = ToyRobot()

    @mock.patch.object(BaseRobot, "robot_get_name")
    @mock.patch.object(BaseRobot, "robot_say_message")
    def test_start(self, mock1, mock2):
        with captured_io(StringIO("ROBBY")) as (out, err):
            self.robby.start()
            mock1.assert_called()
            mock2.assert_called()

    @mock.patch.object(Commands, "exec_command")
    def test_cmd(self, mock):
        with captured_io(StringIO("oFf")) as (out, err):
            self.robby.cmd(World(),Commands(),CommandHandler(Commands().command_dict))
            mock.assert_called()
            

if __name__ == '__main__':
    unittest.main()
