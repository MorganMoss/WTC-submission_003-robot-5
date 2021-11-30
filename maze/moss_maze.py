from .obstacles import *
import random

class Maze():
    
    def __init__(
        self, bounds_x:tuple = (-100,100),
        bounds_y:tuple = (-200, 200), cell_size:int = 4
    ) -> None:
        """
        Constructor for my Maze
        """
        self.maze = Obstacles()
        self.path = []
        offset = cell_size/2

        width = bounds_x[1]//cell_size + bounds_x[1]//cell_size%2
        height = bounds_y[1]//cell_size + bounds_y[1]//cell_size%2

        self.bounds_x, self.bounds_y = (
            (-width, width),
            (-height, height)
        )
        x_range = -width +1, width
        y_range = -height +1, height

        self.nodes = {
            x : { y : False for y in range(*y_range)}
            for x in range(*x_range)
        } 
        
        print(x_range)
        print(y_range)

        self.create_maze(0,0)
        
        for x in range(*x_range):
            for y in range(*y_range):
                if not self.nodes[x][y]:
                    self.maze.add_obstacle(
                        (x*cell_size-offset,y*cell_size-offset),
                        ((x+1)*cell_size-offset,(y+1)*cell_size-offset)
                    )


    def get_maze(self) -> Obstacles():
        return self.maze


    def carve_passage(self, x1,y1,x2,y2):
        if y1 == y2:
            for x in range(x1, x2, -1 if x1 > x2 else 1):
                for y in range(y1, y1+1):
                    self.nodes[x][y] = True
        else:
            for y in range(y1, y2, -1 if y1 > y2 else 1):
                for x in range(x1, x1+1):
                    self.nodes[x][y] = True


    def create_maze(self, x, y):
        while True: #While loop was less restrictive.
            self.path.append((x,y))
            unmarked_found = False
            directions = [(1,0),(-1,0),(0,1),(0,-1)]
            while directions != list():
                direction = directions.pop(random.randint(0, len(directions)-1))
                new_x = x + direction[0]*2
                new_y = y + direction[1]*2

                if  (
                    new_x not in range(self.bounds_x[0]+1,self.bounds_x[1]) 
                    or new_y not in range(self.bounds_y[0]+1,self.bounds_y[1])
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


    """
    def create_maze(self, x, y):
        self.path.append((x,y))
        unmarked_found = False
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        while directions != list():
            direction = directions.pop(random.randint(0, len(directions)-1))
            new_x = x + direction[0]*self.cell_size*2
            new_y = y + direction[1]*self.cell_size*2
            width_low = 1
            width_high = 1

            if  (
                new_x not in range(self.bounds_x[0]+width_low,self.bounds_x[1]-width_high) 
                or new_y not in range(self.bounds_y[0]+width_low,self.bounds_y[1]-width_high)
            ):
                continue
            if self.nodes[new_x][new_y]:
                continue
            unmarked_found = True
            break
        
        if unmarked_found:
            self.carve_passage(x,y,new_x, new_y)
            self.create_maze(new_x, new_y)
        else:
            self.nodes[x][y] = True
            current_node = self.path.index((x,y)) 
            if current_node > 0:
                new_x, new_y = self.path[current_node-1]
                self.create_maze(new_x, new_y)
    #Recursion isn't as fast, and can go to less extreme values
    """