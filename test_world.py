import unittest
from unittest import mock
from obstacles.obstacles import Obstacles
from world.text.world import World
from world.turtle.world import TurtleWorld
from toy_robot.robot_toy import ToyRobot
from io import StringIO
from test_base import captured_io
import math


class TestWorld(unittest.TestCase):
    

    world = World()
    robby = ToyRobot()
    robby.robot.name = 'ROBBY'


    def test_add_robot(self):
        self.world.add_robot(self.robby.robot)
        self.assertEqual(self.world.robot_pos['ROBBY'], (0,0))

    
    def test_get_position(self):
        self.assertEqual(self.world.robot_pos[self.robby.robot.name], (0,0))
        with captured_io(StringIO()) as (out, err): 
            self.world.get_position(self.robby.robot)
        output = out.getvalue()
        self.assertEqual(output, " > ROBBY now at position (0,0).\n")


    def test_rotate_robot(self):
        with captured_io(StringIO()) as (out, err):
            self.world.rotate_robot(self.robby.robot,-90)
            self.assertEqual(self.world.robot_direction[self.robby.robot.name], 270)
            self.world.robot_direction[self.robby.robot.name] = 0
            self.world.rotate_robot(self.robby.robot,90)
            self.assertEqual(self.world.robot_direction[self.robby.robot.name], 90)
            for _ in range(3):
                self.world.rotate_robot(self.robby.robot,90)
            self.assertEqual(self.world.robot_direction[self.robby.robot.name], 0)
        output = out.getvalue()
        self.assertEqual(
""" > ROBBY turned left.
 > ROBBY turned right.
 > ROBBY turned right.
 > ROBBY turned right.
 > ROBBY turned right.
""", output)
        self.world.robot_direction[self.robby.robot.name]


    def test_get_destination(self):
        self.assertEqual(
            self.world.get_destination(self.robby.robot, 10),
            (0,10)
        )
        self.assertEqual(
            self.world.get_destination(self.robby.robot, -10),
            (0,-10)
        )
        self.world.robot_direction["ROBBY"] = 90
        self.assertEqual(
            self.world.get_destination(self.robby.robot, 10),
            (10,0)
        )
        self.assertEqual(
            self.world.get_destination(self.robby.robot, -10),
            (-10,0)
        )



    def test_destination_in_bounds(self):
        with captured_io(StringIO()) as (out, err):
            self.assertFalse(self.world.destination_in_bounds((-101,0)))
            self.assertTrue(self.world.destination_in_bounds((-100,0)))
            self.assertFalse(self.world.destination_in_bounds((0,-201)))
            self.assertTrue(self.world.destination_in_bounds((0,200)))
            self.assertFalse(self.world.destination_in_bounds((-101,201)))
            self.assertTrue(self.world.destination_in_bounds((-100,200)))
            self.assertTrue(self.world.destination_in_bounds((-45,45)))
            self.assertTrue(self.world.destination_in_bounds((45,-45)))

        
    def test_move_robot(self):
        with captured_io(StringIO()) as (out, err):
            for angle in range(0, 361, 90):
                self.world.robot_pos["ROBBY"] = (0,0)
                self.world.robot_direction["ROBBY"] = angle
                angle = math.radians(angle)
                self.world.move_robot(self.robby.robot, 5)
                self.assertEqual(self.world.robot_pos["ROBBY"], 
                                (round(5*math.sin(angle)),round(5*math.cos(angle))))
                self.world.robot_direction["ROBBY"] = 0



class TestTurtleWorld(unittest.TestCase):
    

    world = TurtleWorld()
    robby = ToyRobot()
    robby.robot.name = 'ROBBY'


    def test_add_robot(self):
        self.world.add_robot(self.robby.robot)
        self.assertEqual(self.world.robot_pos['ROBBY'], (0,0))

    
    def test_get_position(self):
        self.assertEqual(self.world.robot_pos[self.robby.robot.name], (0,0))
        with captured_io(StringIO()) as (out, err): 
            self.world.get_position(self.robby.robot)
        output = out.getvalue()
        self.assertEqual(output, " > ROBBY now at position (0,0).\n")


    def test_rotate_robot(self):
        with captured_io(StringIO()) as (out, err):
            self.world.rotate_robot(self.robby.robot,-90)
            self.assertEqual(self.world.robot_direction[self.robby.robot.name], 270)
            self.world.robot_direction[self.robby.robot.name] = 0
            self.world.rotate_robot(self.robby.robot,90)
            self.assertEqual(self.world.robot_direction[self.robby.robot.name], 90)
            for _ in range(3):
                self.world.rotate_robot(self.robby.robot,90)
            self.assertEqual(self.world.robot_direction[self.robby.robot.name], 0)
        output = out.getvalue()
        self.assertEqual(
""" > ROBBY turned left.
 > ROBBY turned right.
 > ROBBY turned right.
 > ROBBY turned right.
 > ROBBY turned right.
""", output)
        self.world.robot_direction[self.robby.robot.name]


    def test_get_destination(self):
        self.assertEqual(
            self.world.get_destination(self.robby.robot, 10),
            (0,10)
        )
        self.assertEqual(
            self.world.get_destination(self.robby.robot, -10),
            (0,-10)
        )
        self.world.robot_direction["ROBBY"] = 90
        self.assertEqual(
            self.world.get_destination(self.robby.robot, 10),
            (10,0)
        )
        self.assertEqual(
            self.world.get_destination(self.robby.robot, -10),
            (-10,0)
        )



    def test_destination_in_bounds(self):
        with captured_io(StringIO()) as (out, err):
            self.assertFalse(self.world.destination_in_bounds((-101,0)))
            self.assertTrue(self.world.destination_in_bounds((-100,0)))
            self.assertFalse(self.world.destination_in_bounds((0,-201)))
            self.assertTrue(self.world.destination_in_bounds((0,200)))
            self.assertFalse(self.world.destination_in_bounds((-101,201)))
            self.assertTrue(self.world.destination_in_bounds((-100,200)))
            self.assertTrue(self.world.destination_in_bounds((-45,45)))
            self.assertTrue(self.world.destination_in_bounds((45,-45)))


    def test_move_robot(self):
        with captured_io(StringIO()) as (out, err):
            for angle in range(0, 361, 90):
                self.world.robot_pos["ROBBY"] = (0,0)
                self.world.robot_direction["ROBBY"] = angle
                angle = math.radians(angle)
                self.world.move_robot(self.robby.robot, 5)
                self.assertEqual(self.world.robot_pos["ROBBY"], 
                                (round(5*math.sin(angle)),round(5*math.cos(angle))))
                self.world.robot_direction["ROBBY"] = 0


if __name__ == '__main__':
    unittest.main()



        