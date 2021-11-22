import unittest
from unittest import mock
from io import StringIO
from test_base import captured_io
from command_handling.commands import Commands
from toy_robot.robot_base import BaseRobot
from world.text.world import World


class TestCommands(unittest.TestCase):
    commands = Commands()
    world = World()
    robot = BaseRobot()
    robot.name = "PAIN"
    world.add_robot(robot)

    def test_exec_command(self):
        for command_name, command in self.commands.command_dict.items():
            world = self.world
            robot = self.robot
            commands = self.commands
            def test_this_command(self, mock):
                l = [command_name]
                if command_name == "OBSTACLES":
                    commands.exec_command(world,robot,l,'')
                elif command_name == "OFF":
                    try:
                        commands.exec_command(world,robot,l,'')
                    except SystemExit: ...
                elif command_name == "REPLAY":
                    l += [('silent', True), ('reversed', False), ('range', range(0))]
                    commands.exec_command(world,robot,l,'')
                else:
                    if 'args' in command.keys():
                        for arg in  command['args']:
                            l += [arg()]
                    if 'optional' in command.keys():
                        for arg in  command['optional']:
                            l += [arg()]
                    commands.exec_command(world,robot,l,'')        
                mock.assert_called()
            with mock.patch.object(Commands, command['command']) as m:
                test_this_command(self, m)


    @mock.patch.object(
        world, 'move_robot', side_effect = lambda s, step  : print(step))
    def test_forward(self, mock):
        self.commands.robot = self.robot
        self.commands.world = self.world
        with captured_io(StringIO()) as (out, err):
            self.commands.command_forward(1)
            mock.assert_called()
            self.commands.command_forward(-1)
            mock.assert_called()
        self.assertEqual(
            "1\n > PAIN now at position (0,0).\n1\n > PAIN now at position (0,0)."
            , out.getvalue().strip())


    @mock.patch.object(
        world, 'move_robot', side_effect = lambda s, step  : print(step))
    def test_back(self, mock):
        self.commands.robot = self.robot
        self.commands.world = self.world
        with captured_io(StringIO()) as (out, err):
            self.commands.command_back(1)
            mock.assert_called()
            self.commands.command_back(-1)
            mock.assert_called()
        self.assertEqual(
            "-1\n > PAIN now at position (0,0).\n-1\n > PAIN now at position (0,0)."
            , out.getvalue().strip())


    @mock.patch.object(
        World, 'move_robot', side_effect = world.move_robot)
    def test_sprint(self, mock):
        self.world.robot_pos[self.robot.name] = (0,0)
        self.world.robot_direction[self.robot.name] = 0

        with captured_io(StringIO()) as (out, err):
            self.commands.command_sprint(2)
            mock.assert_called()
            mock.assert_called()
            self.assertEqual(self.world.robot_pos[self.robot.name] , (0,3))
            self.world.robot_pos[self.robot.name] = (0, 0)            
            self.commands.command_sprint(-3)
            mock.assert_called()
            mock.assert_called()
            self.assertEqual(self.world.robot_pos[self.robot.name] , (0,-6))
            self.world.robot_pos[self.robot.name]  = (0, 0)
    

    @mock.patch.object(
        world, 'rotate_robot', side_effect = world.rotate_robot)
    def test_turn_left(self, mock):
        self.world.robot_direction[self.robot.name] = 0
        with captured_io(StringIO()) as (out, err):
            self.commands.exec_command(self.world, self.robot, ["LEFT"], '')
        self.assertEqual(self.world.robot_direction[self.robot.name], 270)
        output = out.getvalue().strip()
        self.assertIn("> PAIN turned left.", output)
        mock.assert_called()
        self.world.robot_direction[self.robot.name] = 0


    @mock.patch.object(
        world, 'rotate_robot', side_effect = world.rotate_robot)
    def test_turn_right(self, mock):
        self.world.robot_direction[self.robot.name] = 0
        with captured_io(StringIO()) as (out, err):
            self.commands.exec_command(self.world, self.robot,["RIGHT"], '')
        self.assertEqual(self.world.robot_direction[self.robot.name], 90)
        output = out.getvalue().strip()
        self.assertIn("> PAIN turned right.", output)
        mock.assert_called()
        self.world.robot_direction[self.robot.name] = 0

        
    def test_off(self):
        with captured_io(StringIO()) as (out, err):
            try:
                self.commands.command_off()
            except SystemExit:
                ...
        output = out.getvalue().strip()
        self.assertEqual("PAIN: Shutting down..", output)


    def test_help(self):
        self.commands.robot = self.robot
        self.commands.world = self.world
        with captured_io(StringIO()) as (out, err):
            self.commands.command_help()
        output = out.getvalue().strip()
        self.assertIn(
"""I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD\t- Move robot foward by [number] steps
BACK\t- Move robot back by [number] steps
RIGHT\t- Rotate robot right
LEFT\t- Rotate robot left
SPRINT\t- Move robot foward by [number] steps, then [number]-1 steps, and so on, until it hits 0.
HISTORY\t- Shows history of movement commands.
REPLAY\t- Replays previous movement commands.
\t  It has optional arguments:
\t\tSilent - Hides output from replayed commands
\t\tReversed - Reverses the order to be last to first
\t\t<int> - Starts from previous <int> commands
\t\t<int>-<int> - Starts from previous <int> commands and ends at <int> previous commands
OBSTACLES\t- Shows a list of obstacles in current world."""
, output)
    

    def test_replay_get_range(self):
        commands = self.commands
        commands.world = self.world
        commands.robot = self.robot
        commands.history = [[self.world, self.robot, 'abc'] for _ in range(5)]
        good_text = ['4', '2-1']
        bad_text = ['-1','0','1-2','a-2','1--2']
        with captured_io(StringIO()) as (out, err):
            for word in good_text:
                self.assertTrue(commands.replay_get_range(word))
            for word in bad_text:
                self.assertFalse(commands.replay_get_range(word))
        

    def test_replay(self):
        self.commands.history = [
            [self.world, self.robot]+["Forward", 3],[self.world, self.robot]+["Back", 3],[self.world, self.robot]+["Left"]
        ]
        l = [
                "Replay",
                '3-0',
                ('silent', False),
                ('reversed', False)
            ]
        with captured_io(StringIO()) as (out, err):
            self.commands.exec_command(self.world, self.robot, l, '')
        output = out.getvalue()
        self.assertEqual(""" > PAIN moved forward by 3 steps.
 > PAIN now at position (0,3).
 > PAIN moved back by 3 steps.
 > PAIN now at position (0,0).
 > PAIN turned left.
 > PAIN now at position (0,0).
 > PAIN replayed 3 commands.
 > PAIN now at position (0,0).
""", output)

        l[2] = ('silent', True)
        with captured_io(StringIO()) as (out, err):
            self.commands.exec_command(self.world, self.robot, l, '')
        output = out.getvalue()
        self.assertEqual(""" > PAIN replayed 3 commands silently.
 > PAIN now at position (0,0).
""", output)

        l[3] = ('reversed', True)
        with captured_io(StringIO()) as (out, err):
            self.commands.exec_command(self.world, self.robot, l, '')
        output = out.getvalue()
        self.assertEqual(""" > PAIN replayed 3 commands in reverse silently.
 > PAIN now at position (0,0).
""", output)

        l[2] = ('silent', False)
        with captured_io(StringIO()) as (out, err):
            self.commands.exec_command(self.world, self.robot, l, '')
        output = out.getvalue()
        self.assertEqual(""" > PAIN turned left.
 > PAIN now at position (0,0).
 > PAIN moved back by 3 steps.
 > PAIN now at position (0,-3).
 > PAIN moved forward by 3 steps.
 > PAIN now at position (0,0).
 > PAIN replayed 3 commands in reverse.
 > PAIN now at position (0,0).
""", output)

if __name__ == '__main__':
    unittest.main()
