"""
Made by Morgan Moss

░░░░░░░░░▄░░░░░░░░░░░░░░▄░░░░
░░░░░░░░▌▒█░░░░░░░░░░░▄▀▒▌░░░
░░░░░░░░▌▒▒█░░░░░░░░▄▀▒▒▒▐░░░
░░░░░░░▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐░░░
░░░░░▄▄▀▒░▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐░░░
░░░▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▌░░░ 
░░▐▒▒▒▄▄▒▒▒▒░░░▒▒▒▒▒▒▒▀▄▒▒▌░░
░░▌░░▌█▀▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐░░
░▐░░░▒▒▒▒▒▒▒▒▌██▀▒▒░░░▒▒▒▀▄▌░
░▌░▒▄██▄▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒▌░
▐▒▀▐▄█▄█▌▄░▀▒▒░░░░░░░░░░▒▒▒▐░
▐▒▒▐▀▐▀▒░▄▄▒▄▒▒▒▒▒▒░▒░▒░▒▒▒▒▌
▐▒▒▒▀▀▄▄▒▒▒▄▒▒▒▒▒▒▒▒░▒░▒░▒▒▐░
░▌▒▒▒▒▒▒▀▀▀▒▒▒▒▒▒░▒░▒░▒░▒▒▒▌░
░▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▒▄▒▒▐░░
░░▀▄▒▒▒▒▒▒▒▒▒▒▒░▒░▒░▒▄▒▒▒▒▌░░
░░░░▀▄▒▒▒▒▒▒▒▒▒▒▄▄▄▀▒▒▒▒▄▀░░░
░░░░░░▀▄▄▄▄▄▄▀▀▀▒▒▒▒▒▄▄▀░░░░░
░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▀▀░░░░░░░░
"""


import random

from maze.obstacles import Obstacles

maze = None

class Maze():
    
    def __init__(
        self, bounds_x:tuple = (-100,100),
        bounds_y:tuple = (-200, 200), cell_size:int = 4
    ) -> None:
        """
        Constructor for my Maze
        """
        self.cell_size = cell_size
        self.maze:set = set()      
        self.path:list = []
        offset = cell_size/2
        # offset = 0
        width = bounds_x[1]//cell_size + bounds_x[1]//cell_size%2 
        height = bounds_y[1]//cell_size + bounds_y[1]//cell_size%2
        self.x_range = -width + 1, width
        self.y_range = -height + 1, height
        self.nodes = {
            x : { y : False for y in range(*self.y_range)}
            for x in range(*self.x_range)
        } 

        self.create_maze(0,0)

        for x in range(*self.x_range):
            for y in range(*self.y_range):
                if not self.nodes[x][y]:
                    self.maze.add((x*cell_size - offset, y*cell_size - offset))
        
        global maze
        maze = self


    def __str__(self) -> str:
        """
        The to string function for this class

        Returns:
            str: The string made by this class
        """
        string =  ''
        for y in range(*self.y_range):
            row = ''
            for x in range(*self.x_range):
                if not self.nodes[x][-y]:
                    row += 'X'
                else:
                    row += ' '
            string += row + '\n'
        return string


    def generate_obstacles(self) -> list:
        """
        Gets a list of obstacles

        Returns:
            list[tuple(int,int)]: A list of co-ordinates representing obstacles
        """
        return list(self.maze)
       

    def carve_exits(self) -> None:
        """
        Carves exits on each edge of the maze

        Args:
            exit_count (int): Determines the amount of exits carved.
        """

        x1 = random.randint(self.x_range[0],self.x_range[1]-1)
        x2 = random.randint(self.x_range[0],self.x_range[1]-1)
        y1 = random.randint(self.y_range[0],self.y_range[1]-1)
        y2 = random.randint(self.y_range[0],self.y_range[1]-1)
    
        self.carve_passage(x1, self.y_range[0],  x1, self.y_range[0]+2)
        self.carve_passage(x2, self.y_range[1]-1,  x2, self.y_range[1]-3)
        self.carve_passage(self.x_range[0], y1, self.x_range[0]+2, y1)
        self.carve_passage(self.x_range[1]-1, y2, self.x_range[1]-3, y2)

        
    def carve_passage(self, x1:int,y1:int,x2:int,y2:int) -> None:
        """
        Removes the obstacle markers between 2 points.

        Args:
            x1 (int): the x co-ordinate of the first point.
            y1 (int): the y co-ordinate of the first point.
            x2 (int): the x co-ordinate of the second point.
            y2 (int): the y co-ordinate of the second point.
        """
        if y1 == y2:
            for x in range(x1, x2, -1 if x1 > x2 else 1):
                for y in range(y1, y1+1):
                    self.nodes[x][y] = True
        else:
            for y in range(y1, y2, -1 if y1 > y2 else 1):
                for x in range(x1, x1+1):
                    self.nodes[x][y] = True


    def create_maze(self, x:int, y:int) -> None:
        """
        Using backtracking, this function procedurally generates a maze.
        It tunnels in a random direction where it is possible to tunnel. 
        If its not possible to tunnel further, 
        it backtracks its path until it can

        Args:
            x (int): x co-ordinate of the starting point
            y (int): y co-ordinate of the starting point
        """
        while True:
            self.path.append((x,y))

            unmarked_found = False
            directions = [(1,0),(-1,0),(0,1),(0,-1)]
            while directions != list():
                direction = directions.pop(random.randint(0, len(directions)-1))
                new_x = x + direction[0]*2
                new_y = y + direction[1]*2

                if (
                    new_x not in range(*self.x_range) 
                    or new_y not in range(*self.y_range)
                ):
                    continue
                if self.nodes[new_x][new_y]:
                    continue
                unmarked_found = True
                break
            
            if unmarked_found:
                self.carve_passage(x,y,new_x, new_y)
                x,y = new_x, new_y
            else:
                self.nodes[x][y] = True
                current_node = self.path.index((x,y)) 
                if current_node > 0:
                    new_x, new_y = self.path[current_node-1]
                    x,y = new_x, new_y
                    continue
                break

        self.carve_exits()


"""
The below is added to, hopefully, make others lives easier
"""

my_maze = None
cell_size = 0
obstacles = None

def get_obstacles() -> list:
    """
    Gets a list of obstacles,
    but you dont need to initialize an instance of this

    Returns:
        List[tuple[int,int]]: A list of co-ordinates representing obstacles
    """
    global maze, cell_size, obstacles
    if maze != None:
        cell_size = maze.cell_size
        obstacles = maze.generate_obstacles()
    else:
        cell_size = Maze().cell_size
        obstacles = Maze().generate_obstacles()

    obstacles_old = obstacles.copy()
    obstacles = list(map(
        lambda tup : (
            tup, (tup[0] + cell_size, tup[1]+cell_size)), obstacles))
    return obstacles_old


def is_position_blocked(x,y) -> bool:
    """
    Checks if position in an obstacle.

    Args:
        x (int), y (int): 
        the x and y co-ordinates of the new position.

    Returns:
        bool: False if move allowed
    """
    global obstacles
    return  len(list(filter(
        lambda obstacle :
            obstacle[0][0] <= x <= obstacle[1][0] 
            and 
            obstacle[0][1] <= y <= obstacle[1][1]
    , obstacles))) > 0


def is_path_blocked( 
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
                if is_position_blocked(x,y):
                    return True
                x += 1
        else:
            y = (y1 if delta_y > 0 else y2) 
            for i in range(abs(delta_y)): # x = (y-c)/m
                x = (y - constant)/gradient
                if is_position_blocked(x,y):
                    return True
                y += 1

    elif delta_x == 0: #i.e. x = c
        x = x1
        y = (y1 if delta_y > 0 else y2) 
        for _ in range(abs(delta_y)):
            if is_position_blocked(x,y):
                    return True
            y += 1
    else: # delta_y == 0 i.e. y = c
        x = (x1 if delta_x > 0 else x2)
        y = y1
        for _ in range(abs(delta_x)):
            if is_position_blocked(x,y):
                    return True
            x += 1
    return False
