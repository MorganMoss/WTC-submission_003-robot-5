from .obstacles import Obstacles

class Maze():
    
    def __init__(
        self, bounds_x:tuple = (-100,100), 
        bounds_y:tuple = (-200, 200),cell_size:int = 4
    ) -> None:
        """
        Constructor for my Maze. Makes a few random obstacles.
        """
        self.maze = Obstacles()
        self.bounds_x, self.bounds_y = bounds_x, bounds_y
        self.maze.generate_obstacles(self.bounds_x, self.bounds_y)


    def generate_obstacles(self) -> list:
        """
        Gets a list of obstacles

        Returns:
            Obstacles: Obstacles object containing a list of obstacle objects
        """
        return list(map(lambda co_ords : co_ords[0],self.maze))

def generate_obstacles():
    return Maze().generate_obstacles()