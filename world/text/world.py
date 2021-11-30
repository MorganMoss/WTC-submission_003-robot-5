from toy_robot.robot_base import BaseRobot
from maze.obstacles import Obstacles
import math


class World():
    """
    A world for robots to move around in.
    """

    def __init__(
        self, bounds_x:tuple = (-100,100), 
              bounds_y:tuple = (-200,200),
              cell_size:int = 8) -> None:
        """
        Constructor for World.

        Args:
            bounds_x (tuple[int,int], optional):
             Horizontal boundary. Defaults to (-100,100).
            bounds_y (tuple[int,int], optional):
             Vertical boundary. Defaults to (-200,200).
            cell_size (int, optional): Here for turtle world to function
        """
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y
        self.robot_pos = dict()
        self.robot_direction = dict()
        self.obstacles = Obstacles()
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
        self, robot:BaseRobot, start_pos:tuple = (0,0),
        direction:float = 0 ) -> None:
        """
        Adds a robot to this world

        Args:
            robot (BaseRobot): The robot to be added
            start_pos (tuple[int,int], optional): 
            Starting position of the robot. Defaults to (0,0).
            direction (float, optional):
            The direction the robot faces initially. Defaults to 0.
        """
        
        self.robot_pos[robot.name] = start_pos
        self.robot_direction[robot.name] = direction


    def rotate_robot(self, robot:BaseRobot, angle:float) -> None:
        """
        Rotates robot.

        Args:
            robot (BaseRobot): The robot to be rotated.
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



    def get_destination(self, robot:BaseRobot, steps:int) -> tuple:
        """
        Gets the resultant position of the robot.

        Args:
            robot (BaseRobot): The robot to be moved.
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


    def move_robot(self, robot:BaseRobot, steps:int) -> bool:
        """AI is creating summary for move_robot

        Args:
            robot (BaseRobot): The robot to be moved.
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
        
    
    def get_position(self, robot:BaseRobot) -> None:
        """
        Makes robot send a message displaying its current position.
        Args:
            robot (BaseRobot): The robot to display its position.
        """
        robot.robot_say_message(
            f"now at position {str(self.robot_pos[robot.name]).replace(' ', '')}.",
            f" > {robot.name} "
        )

