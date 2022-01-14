from cgitb import small
from functools import reduce
import math
from multiprocessing import connection
from toy_robot import ToyRobot


class World():
    """
    A world for robots to move around in.
    """

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
        self.obstacles = maze(
            bounds_x, bounds_y, cell_size
        ).generate_obstacles()
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
        self.robot_pos = dict()
        self.robot_direction = dict()
        self.cell_size = cell_size


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
        return self.obstacles.obstacles


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

    def find_manhattan_distance(self, x1:int,y1:int,x2:int,y2:int) -> int:
        """
        This function takes in two co-ordinates and calculates it's
        Manhattan Distance (MD). In summary this takes the x and y deltas
        and adds them together

        Args:
            x1, y1 (int): The first point
            x2, y2 (int): The second point

        Returns:
            int: The Manhattan Distance between the points
        """
        return abs(x2-x1) + abs(y2-y1)


    def is_hugging_right(self, robot:ToyRobot) -> bool:
        self.robot_direction[robot.name] = (
            self.robot_direction[robot.name] 
            + 90
        )%360
        destination = self.get_destination(robot, self.cell_size)
        hugging_right = (
            self.obstacles.is_path_blocked(
                *self.robot_pos[robot.name], 
                *destination)
            or not self.destination_in_bounds(destination)
        )
        self.robot_direction[robot.name] = (
            self.robot_direction[robot.name] 
            - 90
        )%360   
        return hugging_right


    def right_hand_algorithm_iteration(self, robot:ToyRobot):
        """
        It does a single iteration of the right hand maze solving algorithm
        on a specific robot, this entials hugging a wall in essence.

        Args:
            robot (ToyRobot): The robot controlled in this process
        """
        if not self.is_hugging_right(robot):
            self.rotate_robot(robot, 90)
            self.move_robot(robot, self.cell_size)
            return
            
        if not self.move_robot(robot, self.cell_size):
            self.rotate_robot(robot, 180)


    def find_productive_path(
        self, robot:ToyRobot, goal_pos:tuple):
        directions = [0,0,0,0]  # up, right, down, left
        
        for i in range(4):
            destination = self.get_destination(robot, self.cell_size)
            if (
                not self.obstacles.is_path_blocked(
                    *self.robot_pos[robot.name], 
                    *destination)
                and self.destination_in_bounds(destination)
            ):
                directions[i]  = self.find_manhattan_distance(
                    *destination,*goal_pos
                )
            self.robot_direction[robot.name] = (
                self.robot_direction[robot.name] 
                + 90
            )%360
        
        shortest = reduce(
            lambda a,b : a if b>a else b,
            filter(lambda x : x > 0, directions)
        ) 

        smallest_manhattan_distance = self.find_manhattan_distance(
                    *self.robot_pos[robot.name],*goal_pos
                )
        if shortest < smallest_manhattan_distance and shortest > 0:
            return shortest, directions.index(shortest)
        else:
            return False


    def solve_to_pos(self, robot:ToyRobot, goal_pos:tuple):
        
        robot.messages_enabled = False
        index = 0 if goal_pos[0] else 1
        if index:
            for x in range(self.bounds_x[0]+1, self.bounds_x[1]-2, self.cell_size):
                if not (x, goal_pos[1]) in self.obstacles.obstacles:
                    goal_pos = (x, goal_pos[1])
                    break

        else:
            for y in range(self.bounds_y[0]+1, self.bounds_y[1]-2, self.cell_size):
                if not (goal_pos[0], y) in self.obstacles.obstacles:
                    goal_pos = (goal_pos[0], y)
                    break
        
        lenience = range(goal_pos[index]-self.cell_size+2, goal_pos[index]+self.cell_size-1)

        smallest_manhattan_distance = self.find_manhattan_distance(
            *self.robot_pos[robot.name],*goal_pos
        )
        # while self.robot_pos[robot.name][index] != goal_pos[index]:
        while not self.robot_pos[robot.name][index] in lenience:
            productive_path = self.find_productive_path(robot, goal_pos)
            if productive_path:
                self.rotate_robot(robot, 90*productive_path[1])
                self.move_robot(robot, self.cell_size)
                self.rotate_robot(robot, -90*productive_path[1])
            else:
                smallest_manhattan_distance = self.find_manhattan_distance(
                    *self.robot_pos[robot.name],*goal_pos
                )

                rotation = - self.robot_direction[robot.name]
                if index:
                    if goal_pos[1] < 0:
                        rotation -= 180
                else:
                    if goal_pos[0] < 0:
                        rotation -= 90
                    else:
                        rotation += 90
                rotation -= 90
                self.rotate_robot(robot, rotation)
                self.move_robot(robot, self.cell_size)

                while not (
                    self.find_productive_path(robot, goal_pos) 
                    and self.find_manhattan_distance(
                        *self.robot_pos[robot.name]
                        ,*goal_pos
                    ) == smallest_manhattan_distance
                ):
                    self.right_hand_algorithm_iteration(robot)
        robot.messages_enabled = True
