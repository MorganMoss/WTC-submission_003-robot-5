from maze.obstacles import *
import unittest
import random


class TestObstacles(unittest.TestCase):
    def test_constructor(self):
        obs = Obstacles()
        self.assertEqual(obs, set())


    def test_add_obstacle(self):
        obs = Obstacles()
        ob1 = (0,0)
        ob2 = (5,2)
        ob3 = (-15,-3)
        obs.add_obstacle(ob1)
        obs.add_obstacle(ob2)
        obs.add_obstacle(ob3)
        obs.add_obstacle((2,4))
        self.assertEqual(len(obs), 4)


    def test_to_str(self):
        obs = Obstacles()
        ob1 = (0,0)
        ob2 = (5,2)
        ob3 = (-15,-3)
        obs.add_obstacle(ob1)
        obs.add_obstacle(ob2)
        obs.add_obstacle(ob3)
        obs.add_obstacle((2,4))
        s =  {"- At position 0,0 (to 4,4)",
            "- At position 5,2 (to 9,6)",
            "- At position -15,-3 (to -11,1)",
            "- At position 2,4 (to 6,8)"}
        o = str(obs)
        for i in s:
            self.assertIn(i, o)
            o = o.replace(i, "")
        self.assertEqual(o.strip(), '')
    

    def test_add_random_obstacle(self):
        obs = Obstacles()
        random.randint = lambda a, b: 1
        obs.add_random_obstacle((1,1),(1,1))
        self.assertEqual(obs.pop()[0], (1,1))
        random.randint = lambda a, b: 0
        obs.add_random_obstacle((0,0),(0,0))
        self.assertEqual(len(obs), 0)


        
    def test_generate_obstacles(self):
        obs = Obstacles()
        obs.generate_obstacles((1,1),(1,1))
        for ob in obs:
            self.assertEqual(ob[0], (1,1))


    def test_is_position_blocked(self):
        self.obs = Obstacles()
        self.obs.add_obstacle((1,1))

        self.assertTrue(self.obs.is_position_blocked(*(1,1)))
        self.assertTrue(self.obs.is_position_blocked(*(5,5)))
        self.assertTrue(self.obs.is_position_blocked(*(1,5)))
        self.assertTrue(self.obs.is_position_blocked(*(5,1)))

        self.assertFalse(self.obs.is_position_blocked(*(0,1)))
        self.assertFalse(self.obs.is_position_blocked(*(1,0)))
        self.assertFalse(self.obs.is_position_blocked(*(5,0)))
        self.assertFalse(self.obs.is_position_blocked(*(0,5)))
        self.assertFalse(self.obs.is_position_blocked(*(6,6)))
        self.assertFalse(self.obs.is_position_blocked(*(0,0)))
        self.assertFalse(self.obs.is_position_blocked(*(0,6)))
        self.assertFalse(self.obs.is_position_blocked(*(6,0)))

        self.obs = Obstacles()
        

    def test_path_blocked(self):
        self.obs = Obstacles()
        
        self.obs.add_obstacle((0,10))
        self.assertTrue(
            self.obs.is_path_blocked(*(0,0), *(0,20)))
        self.assertFalse(
            self.obs.is_path_blocked(*(0,0), *(0,9)))
        self.obs = Obstacles()

        self.obs.add_obstacle((0,-10))
        self.assertTrue(
            self.obs.is_path_blocked(*(0,0), *(0,-20)))
        self.assertFalse(
            self.obs.is_path_blocked(*(0,0), *(0,-5)))
        self.obs = Obstacles()

        self.obs.add_obstacle((10,0))
        self.assertTrue(
            self.obs.is_path_blocked(*(0,0), *(20,0)))
        self.assertFalse(
            self.obs.is_path_blocked(*(0,0), *(9,0)))
        self.obs = Obstacles()

        self.obs.add_obstacle((-10,0))
        self.assertTrue(
            self.obs.is_path_blocked(*(0,0), *(-20,0)))
        self.assertFalse(
            self.obs.is_path_blocked(*(0,0), *(-5,0)))
        self.obs = Obstacles()

        self.obs.add_obstacle((10,10))
        self.assertTrue(
            self.obs.is_path_blocked(*(0,0), *(20,20)))
        self.assertFalse(
            self.obs.is_path_blocked(*(0,0), *(9,9)))
        self.obs = Obstacles()

        self.obs.add_obstacle((-10,-10))
        self.assertTrue(
            self.obs.is_path_blocked(*(0,0), *(-20,-20)))
        self.assertFalse(
            self.obs.is_path_blocked(*(0,0), *(-5,-5)))
        self.obs = Obstacles()


if __name__ == '__main__':
    unittest.main()
