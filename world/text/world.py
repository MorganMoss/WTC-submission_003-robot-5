from cmath import inf
import math
from modulefinder import Module
from sys import setrecursionlimit
from maze.obstacles import Obstacles
from toy_robot import ToyRobot


class World():
    """
    A world for robots to move around in.
    """

    def handle_obstacles(self, maze:Module):
        """
        This is to translate what I get from other's mazes 
        to work well with my mazerunner.

        Args:
            maze (Module): The maze being used
        """
        old_cell_size = self.cell_size
        
        self.maze = list(set(map(lambda item : tuple(item), maze.get_obstacles())))

        smallest = inf
        try :
            maze.my_maze
        except AttributeError:
            for obstacle_1 in self.maze:
                for obstacle_2 in self.maze:
                    if obstacle_1 != obstacle_2:
                        if obstacle_1[1] == obstacle_2[1]:
                            smallest = min(smallest, abs(obstacle_1[0] - obstacle_2[0]))
                        elif obstacle_1[0] == obstacle_2[0]:
                            smallest = min(smallest, abs(obstacle_1[1] - obstacle_2[1]))
            if smallest != inf:
                self.cell_size = int(smallest)


        low_x = 0
        high_x = 0
        low_y = 0
        high_y = 0

        for obstacle in self.maze:
            if obstacle[0]%self.cell_size == 0:
                obstacle =int(obstacle[0] + self.cell_size/2), obstacle[1]
            if obstacle[1]%self.cell_size == 0:
                obstacle =obstacle[0], int(obstacle[1] + self.cell_size/2)

            self.obstacles.add_obstacle(
                obstacle, (obstacle[0] + self.cell_size, obstacle[1] + self.cell_size))
            low_x =  min(low_x, obstacle[0])
            high_x = max(high_x, obstacle[0]+ self.cell_size)
            low_y =  min(low_y, obstacle[1])
            high_y = max(high_y, obstacle[1]+ self.cell_size)

        if not(high_x < 10 or low_x > -10 or high_y < 10 or low_y > -10):
            self.bounds_x = (int(low_x), int(high_x))
            self.bounds_y = (int(low_y), int(high_y))
        else:
            self.cell_size = old_cell_size


    def pixelate_obstacles(self, maze:Module):
        """
        This turns the maze into a 2d grid of 1's and 0's to make solving easier
        Args:
            maze (Module): The maze being used
        """
        self.maze = sorted(self.maze, key = lambda a : a[1])
        self.maze = sorted(self.maze, key = lambda a : a[0])
        
        for i in range(len(self.maze)):
            if self.maze[i][0]%self.cell_size == 0:
                self.maze[i] = int(self.maze[i][0] + self.cell_size/2), self.maze[i][1]
            if self.maze[i][1]%self.cell_size == 0:
                self.maze[i] = self.maze[i][0], int(self.maze[i][1] + self.cell_size/2)

        self.map_of_maze:dict = dict()

        offset = -0.5

        self.x_range = list(range(self.bounds_x[0], self.bounds_x[1], self.cell_size))
        self.x_range.reverse()
        self.y_range = range(self.bounds_y[0], self.bounds_y[1], self.cell_size)

        for x in self.x_range:
            self.map_of_maze[int((x/self.cell_size)-offset)] = dict()
            for y in self.y_range:
                if (x,y) in self.maze:
                    self.map_of_maze[int((x/self.cell_size)-offset)][int((y/self.cell_size)-offset)] = 1
                else:
                    self.map_of_maze[int((x/self.cell_size)-offset)][int((y/self.cell_size)-offset)] = 0


    def __init__(
        self, maze: type,
        bounds_x:tuple = (-100,100), 
        bounds_y:tuple = (-200,200),
        cell_size:int = 8
        ) -> None:
        """
        Constructor for World.

        Args:
            maze (type): a Maze generator that returns a list of obstacles
            bounds_x (tuple[int,int], optional):
             Horizontal boundary. Defaults to (-100,100).
            bounds_y (tuple[int,int], optional):
             Vertical boundary. Defaults to (-200,200).
            cell_size (int, optional): Here for turtle world to function
        """
        self.obstacles:Obstacles = Obstacles()
        self.bounds_x:tuple = bounds_x
        self.bounds_y:tuple = bounds_y
        self.cell_size:int = cell_size
        self.robot_pos = dict()
        self.robot_direction = dict()
        self.handle_obstacles(maze)
        self.pixelate_obstacles(maze)


    def __str__(self) -> str:
        """The str method for this class

        Returns:
            str: Gives info about the obstacles
        """
        return str(self.obstacles)

    def draw_obstacles(self) -> None:
        """
        Does nothing, is place holder for turtle world
        """
        ...


    def get_obstacles(self) -> list:
        """
        Gets a list of the obstacles inside this world.

        Returns:
            list[Obstacles]: A list of Obstacles in this world.
        """
        return self.obstacles


    def generate_obstacles(self) -> None:
        """
        Creates up to 10 randomly placed obstacles in this world.
        """
        self.obstacles.generate_obstacles(self.bounds_x, self.bounds_y)


    def add_robot(
        self, robot:ToyRobot, start_pos:tuple = (0,0),
        direction:float = 0 ) -> None:
        """
        Adds a robot to this world

        Args:
            robot (ToyRobot): The robot to be added
            start_pos (tuple[int,int], optional): 
            Starting position of the robot. Defaults to (0,0).
            direction (float, optional):
            The direction the robot faces initially. Defaults to 0.
        """
        # while self.obstacles.is_position_blocked(*start_pos):
        #     start_pos = (
        #         int(random.randint(-5,5)*self.cell_size/2),
        #         int(random.randint(-5,5)*self.cell_size/2)
        #     )
        self.robot_pos[robot.name] = start_pos
        self.robot_direction[robot.name] = direction


    def rotate_robot(self, robot:ToyRobot, angle:float) -> None:
        """
        Rotates robot.

        Args:
            robot (ToyRobot): The robot to be rotated.
            angle (float): The degrees by which it rotates.
        """
        direction =  'right' if angle > 0 else 'left'

        self.robot_direction[robot.name] = (
            self.robot_direction[robot.name] 
            + angle
        )%360
        
        robot.robot_say_message(
            f"turned {direction}.",
            f" > {robot.name} "
        )


    def get_destination(self, robot:ToyRobot, steps:int) -> tuple:
        """
        Gets the resultant position of the robot.

        Args:
            robot (ToyRobot): The robot to be moved.
            steps (int): The distance the robot moves.

        Returns:
            tuple[int,int]: the x and y co-ordinates of the new position.
        """
        return  (
                    self.robot_pos[robot.name][0]
                    + round(steps*math.sin(
                        math.radians(self.robot_direction[robot.name]))),
                        
                    self.robot_pos[robot.name][1]
                    + round(steps*math.cos(
                        math.radians(self.robot_direction[robot.name])))
                )
    

    def destination_in_bounds(self, destination:tuple) -> bool:
        """
        Checks if the robot will move into a boundary

        Args:
            destination (tuple[int,int]):
            the x and y co-ordinates of the new position.

        Returns:
            bool: True if move is allowed.
        """
        return  (self.bounds_x[0] <= destination[0] <= self.bounds_x[1]) \
                and (self.bounds_y[0] <= destination[1] <= self.bounds_y[1])


    def move_robot(self, robot:ToyRobot, steps:int) -> bool:
        """AI is creating summary for move_robot

        Args:
            robot (ToyRobot): The robot to be moved.
            steps (int): The distance the robot moves

        Returns:
            bool:  True if the move was successful
        """

        destination = self.get_destination(robot, steps)

        if destination == self.robot_pos[robot.name]:
            robot.robot_say_message(
                f" > {robot.name} moved forward by 0 steps.",
            )
            return False

        if not self.destination_in_bounds(destination):
            robot.robot_say_message(
                "Sorry, I cannot go outside my safe zone.",
                f"{robot.name}: "
            )
            return False

        if self.obstacles.is_path_blocked(*self.robot_pos[robot.name], *destination):
            robot.robot_say_message(
                "Sorry, there is an obstacle in the way.",
                f"{robot.name}: "
            )
            return False

        self.robot_pos[robot.name] = destination

        direction = "forward" if steps >= 0 else "back"
        robot.robot_say_message(
            f"moved {direction} by {abs(steps)} steps.",
            f" > {robot.name} "
        )
        return True
        
    
    def get_position(self, robot:ToyRobot) -> None:
        """
        Makes robot send a message displaying its current position.
        Args:
            robot (ToyRobot): The robot to display its position.
        """
        robot.robot_say_message(
            f"now at position {str(self.robot_pos[robot.name]).replace(' ', '')}.",
            f" > {robot.name} "
        )
    

    def explore_zeros(self, x:int, y:int):
        """
        Gives a number to all the items
        assigned 0 surrounding the current co-ords.

        Args:
            x (int): x co-ord of position
            y (int): y co-ord of position
        """
            
        val = self.map_of_maze[x][y] 
        if x > min(*self.map_of_maze.keys()) and not self.map_of_maze[x-1][y]:
            self.map_of_maze[x-1][y] = val + 1
            self.explore_zeros(x-1,y)

        if x < max(*self.map_of_maze.keys()) and not self.map_of_maze[x+1][y]:
            self.map_of_maze[x+1][y] = val + 1
            self.explore_zeros(x+1,y)

        if y > min(*self.map_of_maze[0].keys()) and not self.map_of_maze[x][y-1]:
            self.map_of_maze[x][y-1] = val + 1
            self.explore_zeros(x,y-1) 

        if y < max(*self.map_of_maze[0].keys()) and not self.map_of_maze[x][y+1]:
            self.map_of_maze[x][y+1] = val + 1
            self.explore_zeros(x,y+1)


    def backtrace(self, x:int, y:int):
        """
        Starts at the end goal and traces to the
        next pos with a number = the current number -1

        Args:
            x (int): x co-ord of position
            y (int): y co-ord of position
        """
        val = self.map_of_maze[x][y]

        if val == 2:
            self.map_of_maze[x][y] = 0

        if val >= 3:
            val -= 1

            if x > min(*self.map_of_maze.keys()) and self.map_of_maze[x-1][y] == val:
                self.path.append(((x-1)*self.cell_size,y*self.cell_size))
                self.backtrace(x-1,y)

            elif x < max(*self.map_of_maze.keys()) and self.map_of_maze[x+1][y] == val:
                self.path.append(((x+1)*self.cell_size,y*self.cell_size))
                self.backtrace(x+1,y)

            elif y > min(*self.map_of_maze[0].keys()) and self.map_of_maze[x][y-1] == val:
                self.path.append((x*self.cell_size,(y-1)*self.cell_size))
                self.backtrace(x,y-1)

            elif y < max(*self.map_of_maze[0].keys()) and self.map_of_maze[x][y+1] == val:
                self.path.append((x*self.cell_size,(y+1)*self.cell_size))
                self.backtrace(x,y+1)


    def mazerun(self, robot:ToyRobot, goal_pos:tuple):
        """
        Solves the maze by mapping it out. This is faster.

        Args:
            robot (ToyRobot): The robot to be moved around
            goal_pos (tuple): The edge to land on
        """
        setrecursionlimit(10**7) 

        map_of_maze = dict()
        for x, y in self.map_of_maze.items():
            map_of_maze[x] = y.copy()
        
        offset = -0.5
        self.index = 0 if goal_pos[0] else 1

        robot_x = int(self.robot_pos[robot.name][0]/self.cell_size-offset)
        robot_y = int(self.robot_pos[robot.name][1]/self.cell_size-offset)

        self.map_of_maze[robot_x][robot_y] = 2
        try:
            self.explore_zeros(robot_x, robot_y)
        except Exception as e:
            print(e)
        

        shortest_path = inf
        shortest_path_co_ords = (robot_x, robot_y)
            

        if self.index:
            y = min(*self.map_of_maze[0].keys()) if goal_pos[1]<0 else max(*self.map_of_maze[0].keys())
            for x in self.map_of_maze.keys():
                if self.map_of_maze[x][y] > 1:
                    if shortest_path > self.map_of_maze[x][y]:
                        shortest_path = self.map_of_maze[x][y]
                        shortest_path_co_ords = x,y
        else:
            x = min(*self.map_of_maze.keys()) if goal_pos[0]<0 else max(*self.map_of_maze.keys())
            for y in self.map_of_maze[0].keys():
                if self.map_of_maze[x][y] > 1:
                    if shortest_path > self.map_of_maze[x][y]:
                        shortest_path = self.map_of_maze[x][y]
                        shortest_path_co_ords = x,y

        self.path = list()
        if shortest_path < inf:
            self.backtrace(*shortest_path_co_ords)
        else:
            robot.robot_say_message(
                f"Unable to solve to this edge, Sowwy ;w;",
                f" > {robot.name} "
            )

        self.path.reverse()

        self.path.append((shortest_path_co_ords[0]*self.cell_size, shortest_path_co_ords[1]*self.cell_size))
            
        self.map_of_maze = dict()
        for x, y in map_of_maze.items():
            self.map_of_maze[x] = y.copy()
        
        setrecursionlimit(10**3) 

        return self.path


    def enable_keys(self) -> None:
        """
        Placeholder for Turtle World
        """
        print("This only works on Turtle!")