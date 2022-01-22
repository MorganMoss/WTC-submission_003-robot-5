from maze.moss_maze import Maze
import unittest


class TestMaze(unittest.TestCase):
    def test_constructor(self):

        maze= Maze((-10,10),(-10,10),2)
        self.assertTrue(type(maze.maze) == set)
        #going to be used in range(), therefore 2nd term needs to be n+1
        self.assertEqual(maze.x_range ,(-5,5+1))
        self.assertEqual(maze.y_range ,(-5,5+1))

        self.assertEqual(
            maze.nodes.keys(),
            {-5,-4,-3,-2,-1,0,1,2,3,4,5}
        )
        for value in maze.nodes.values():
            self.assertEqual(
                value.keys(),
                {-5,-4,-3,-2,-1,0,1,2,3,4,5}
            )
        for value in maze.nodes.values():
            for value_2 in value.values():
                self.assertEqual(
                    type(value_2),
                    bool
                )


    def test_to_str(self):
        maze= Maze((-10,10),(-10,10),2)
        
        s = str(maze).strip('\n').split('\n')
        for line in s:
            self.assertEqual(len(line), 11)
            for char in line:
                self.assertTrue(char == ' ' or char == 'X')
            self.assertIn(' ', line)
            self.assertIn('X', line)


    def test_generate_obstacles(self):
        maze= Maze((-10,10),(-10,10),2)
        for co_ord in maze.generate_obstacles():
            self.assertEqual(type(co_ord), tuple)
            self.assertEqual(len(co_ord), 2)


if __name__ == '__main__':
    unittest.main()
