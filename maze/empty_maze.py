from .obstacles import *
import random

class Maze():
    
    def __init__(
        self, bounds_x:tuple = (-100,100), 
        bounds_y:tuple = (-200, 200),cell_size:int = 4
    ) -> None:
        """
        Constructor for my Maze
        """
        self.maze = Obstacles()
        self.bounds_x, self.bounds_y = bounds_x, bounds_y
        self.maze.generate_obstacles(self.bounds_x, self.bounds_y)


    def get_maze(self) -> Obstacles():
        return self.maze

