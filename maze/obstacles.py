import random


class Obstacle():
    """
    A data type - Single obstacle, for use in Obstacles.
    """

    def __init__(self, pos:tuple, end_pos:tuple = None) -> None:
        """
        Constructor for individual Obstacle

        Args:
            pos (tuple[int,int]): x, y co-ordinates of the bottom left corner
            end_pos (tuple[int,int]): x, y co-ordinates of the top right corner

        """
        self.pos = pos

        if end_pos != None:
            self.end_pos = end_pos
        else:
            self.end_pos = pos[0]+4, pos[1]+4


    def __str__(self) -> str:
        """
        Creates a string for this obstacle, 
        the co-ords of the bottom left and top right corners.

        Returns:
            str: The string representing this obstacle.
        """
        return  (f"- At position {self.pos[0]},{self.pos[1]}"+ 
                f" (to {self.end_pos[0]},{self.end_pos[1]})")

    
class Obstacles():
    """ 
    Is a container that holds and manages obstacles.
    """


    def __init__(self) -> None:
        """
        Initialises the Obstacle container
        """
        self.obstacles:set = set()


    def __str__(self) -> str:
        """
        Returns a string represting the list of 
        obstacles contained in this Obstacles instance.

        Returns:
            str: Obstacles, separated by '/n'.
        """
        return "\n".join(map(str, self.obstacles))

    
    def add_obstacle(
        self, pos:tuple = None, end_pos:tuple = None, 
        obstacle:Obstacle = None
    ) -> None:
        """
        Adds an obstacle via given object or by set of co-ords

        Args:
            pos (tuple[int,int], optional): Add obstacle via co-ords. 
            Defaults to None.
            end_pos (tuple[int,int], optional): End co-ords for obstacle.
            Defaults to None.
            obstacle (Obstacle, optional): Add already created obstacle. 
            Defaults to None.
        """
        if pos != None:
            self.obstacles.add(
                Obstacle(((pos[0]), (pos[1])), ((end_pos[0]), (end_pos[1]))))
        if obstacle != None:
            self.obstacles.add(obstacle)


    def generate_obstacles(
        self, bounds_x:tuple, bounds_y:tuple
    ) -> None:
        """
        Generates up to 10 obstacles in random places within bounds

        Args:
            bounds_x (tuple[int,int]): Horizontal boundaries of area
            bounds_y (tuple[int,int]): Vertical bondaries of area
        """
        for _ in range(random.randint(0,10)):
            self.add_random_obstacle(bounds_x,bounds_y)


    def add_random_obstacle(
        self, bounds_x:tuple, bounds_y:tuple
    ) -> None:
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


    def get_obstacles(self) -> list:
        """
        Get's this containers list of obstacles.

        Returns:
            list[Obstacle]: The list of obstacles in this container.
        """
        return self.obstacles


    def is_position_blocked(self, x,y) -> bool:
        """
        Checks if position in an obstacle.

        Args:
            x (int), y (int): 
            the x and y co-ordinates of the new position.

        Returns:
            bool: False if move allowed
        """
        return  len(list(filter(
            lambda obstacle :
                obstacle.pos[0] <= x <= obstacle.end_pos[0] 
                and 
                obstacle.pos[1] <= y <= obstacle.end_pos[1]
        , self.obstacles))) > 0


    def is_path_blocked(self, 
        x1:int, y1:int,
        x2:int, y2:int
    ) -> bool:
        """
        Checks if there is an obstacle between the robot and it's destination.

        Args:
            x1 (int), y1 (int):
            the x and y co-ordinates of the start position.
            x2 (int), y2 (int):
            the x and y co-ordinates of the end position.
            
        Returns:
            bool: False is move is allowed
        """
        delta_x = x2 - x1
        delta_y = y2 - y1

        if delta_x != 0 and delta_y != 0: 
            gradient =  delta_y/delta_x
            constant = y1 - gradient*x1 
            if delta_x >= delta_y:
                x = (x1 if delta_x > 0 else x2)
                for i in range(abs(delta_x)): #y = mx+c
                    y = gradient*x +constant
                    if self.is_position_blocked(x,y):
                        return True
                    x += 1
            else:
                y = (y1 if delta_y > 0 else y2) 
                for i in range(abs(delta_y)): # x = (y-c)/m
                    x = (y - constant)/gradient
                    if self.is_position_blocked(x,y):
                        return True
                    y += 1

        elif delta_x == 0: #i.e. x = c
            x = x1
            y = (y1 if delta_y > 0 else y2) 
            for _ in range(abs(delta_y)):
                if self.is_position_blocked(x,y):
                        return True
                y += 1
        else: # delta_y == 0 i.e. y = c
            x = (x1 if delta_x > 0 else x2)
            y = y1
            for _ in range(abs(delta_x)):
                if self.is_position_blocked(x,y):
                        return True
                x += 1
        return False
