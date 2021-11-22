import random


class Obstacle():
    """
    A data type - Single obstacle, for use in Obstacles.
    """

    def __init__(self, pos:tuple[int,int]) -> None:
        """
        Constructor for individual Obstacle

        Args:
            pos (tuple[int,int]): x, y co-ordinates of the bottom left corner
        """
        self.pos = pos


    def __str__(self) -> str:
        """
        Creates a string for this obstacle, 
        the co-ords of the bottom left and top right corners.

        Returns:
            str: The string representing this obstacle.
        """
        return  (f"- At position {self.pos[0]},{self.pos[1]}"+ 
                f" (to {self.pos[0]+4},{self.pos[1]+4})")

    
class Obstacles():
    """ 
    Is a container that holds and manages obstacles.
    """


    def __init__(self) -> None:
        """
        Initialises the Obstacle container
        """
        self.obstacles:list[Obstacle] = list()


    def __str__(self) -> str:
        """
        Returns a string represting the list of 
        obstacles contained in this Obstacles instance.

        Returns:
            str: Obstacles, separated by '/n'.
        """
        return "\n".join(map(str, self.obstacles))

    
    def add_obstacle(self, pos:tuple[int,int] = None, obstacle:Obstacle = None) -> None:
        """AI is creating summary for add_obstacle

        Args:
            pos (tuple[int,int], optional): Add obstacle via co-ords. Defaults to None.
            obstacle (Obstacle, optional): Add already created obstacle. Defaults to None.
        """
        if pos != None:
            self.obstacles.append(Obstacle(pos))
        if obstacle != None:
            self.obstacles.append(obstacle)


    def generate_obstacles(
        self, bounds_x:tuple[int,int], bounds_y:tuple[int,int]) -> None:
        """
        Generates up to 10 obstacles in random places within bounds

        Args:
            bounds_x (tuple[int,int]): Horizontal boundaries of area
            bounds_y (tuple[int,int]): Vertical bondaries of area
        """
        for _ in range(random.randint(0,10)):
            self.add_random_obstacle(bounds_x,bounds_y)


    def add_random_obstacle(
        self, bounds_x:tuple[int,int], bounds_y:tuple[int,int]) -> None:
        """
        Creates a randomly placed obstacle and adds it to obstacles 

        Args:
            bounds_x (tuple[int,int]): Horizontal boundaries of area
            bounds_y (tuple[int,int]): Vertical bondaries of area
        """
        pos = (random.randint(*bounds_x), random.randint(*bounds_y))
        while pos in map(lambda obstacle: obstacle.pos, self.obstacles):
            pos = (random.randint(*bounds_x), random.randint(*bounds_y))
        if pos != (0,0):
            self.add_obstacle(pos)


    def is_position_blocked(self, destination:tuple) -> bool:
        """
        Checks if position in an obstacle.

        Args:
            destination (tuple[int,int]):
            the x and y co-ordinates of the new position.

        Returns:
            bool: False if move allowed
        """
        return  len(list(filter(
            lambda obstacle :
                obstacle.pos[0] <= destination[0] <= obstacle.pos[0]+4 
                and 
                obstacle.pos[1] <= destination[1] <= obstacle.pos[1]+4
        , self.obstacles))) > 0

    
    def is_path_blocked(
        self, start:tuple, destination:tuple) -> bool:
        """
        Checks if there is an obstacle between the robot and it's destination.

        Args:
            robot (BaseRobot): The robot to be moved.
            destination (tuple[int,int]):
            the x and y co-ordinates of the new position.

        Returns:
            bool: False is move is allowed
        """
        delta_x = destination[0] - start[0]
        delta_y = destination[1] - start[1]

        if delta_x != 0 and delta_y != 0: 
            gradient =  delta_y/delta_x
            constant = start[1] - gradient*start[0] 
            if delta_x >= delta_y:
                x = (start[0] if delta_x > 0 else destination[0])
                for i in range(abs(delta_x)): #y = mx+c
                    y = gradient*x +constant
                    if self.is_position_blocked((x,y)):
                        return True
                    x += 1
            else:
                y = (start[1] if delta_y > 0 else destination[1]) 
                for i in range(abs(delta_y)): # x = (y-c)/m
                    x = (y - constant)/gradient
                    if self.is_position_blocked((x,y)):
                        return True
                    y += 1

        elif delta_x == 0: #i.e. x = c
            x = start[0]
            y = (start[1] if delta_y > 0 else destination[1]) 
            for _ in range(abs(delta_y)):
                if self.is_position_blocked((x,y)):
                        return True
                y += 1
        else: # delta_y == 0 i.e. y = c
            x = (start[0] if delta_x > 0 else destination[0])
            y = start[1]
            for _ in range(abs(delta_x)):
                if self.is_position_blocked((x,y)):
                        return True
                x += 1
        return False
